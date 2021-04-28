from sys import path
from os import name as os_name, getenv, mkdir
from os.path import isdir, abspath, exists
from subprocess import call
from time import sleep, time
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger
from multiprocessing import Process
from glob import glob

from t_bot.bot_handler import BotHandler
from utils.courses import scrap_currency_from_page, get_pycbrf_course
from utils.take_photo import photo
from devices import video

if os_name != 'nt':
    # TODO change to dynamic
    path.append("/home/pi/d_sh_handler")
    PHOTO_DIR = "/home/pi/d_sh_handler/photos"
    VIDEO_DIR = "/home/pi/d_sh_handler/videos"
else:
    PHOTO_DIR = abspath('./photos')
    VIDEO_DIR = abspath('./videos')

if isdir(PHOTO_DIR) is False:
    mkdir(PHOTO_DIR)
if isdir(VIDEO_DIR) is False:
    mkdir(VIDEO_DIR)


def get_currency(command:str) -> str:
    pycbrf_todays_currency = get_pycbrf_course(command.upper())
    moex_answer = scrap_currency_from_page(command.upper())
    message = f"1 {command.upper()} = {pycbrf_todays_currency} RUB CBRF, {moex_answer} RUB Moex"
    return message


def set_volume(param:str) -> str:
    logger.info("Управление звуком зарегистрировано")
    if os_name != 'nt':
        volume = param
        if volume.isdigit():
            int_volume = int(volume)
            if int_volume > 100:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '100%'])
                message = f"Ставлю звук на максимум({audio_answer})"
            elif int_volume < 0:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
                message = f"Выключаю звук({audio_answer})"
            else:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', f'{int_volume}%'])
                message = f"Ставлю звук на {int_volume}({audio_answer})"
        else:
            audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
            message = f"Команда не распознана до конца, выключаю звук({audio_answer})"
    else:
        message = "Не та ОС"

    # self.bot.send_message(chat, message)
    logger.info(message)
    return message


def send_greetings(name, time_now) -> str:
    if 6 <= time_now < 12:
        msg = f"Доброе утро, {name}."
    elif 12 <= time_now < 18:
        msg = f"Добрый день, {name}."
    elif 18 <= time_now < 23:
        msg = f"Добрый вечер, {name}."
    else:
        msg = f"{name}, пора спать."
    return msg


class MainBot:
    def __init__(self):
        logger.info("Started bot")
        if not load_dotenv():
            logger.info("Problem with .env")
            raise BaseException

        token = getenv('MY_TOKEN')
        self.admin_id = getenv('ADMIN_ID')
        self.valid_chats = [int(_) for _ in getenv("TRUST_ID")]

        self.photo_dir = PHOTO_DIR
        self.video_dir = VIDEO_DIR

        self.bot = BotHandler(token)

        self.bot_key = '/'
        self.admin_commands = ('add_chat_id', 'show_active_chats')
        self.admin_reboot_device_commands = ('reboot', 'r')
        self.renew_ver_git_commands = ('git_renew', 'update')

        self.currency_commands = ("eur", "usd")
        self.currency_set_correct = ("EUR", "USD")
        self.greetings_commands = ('hello', 'hi', 'qq', 'greetings')
        self.light_commands = ('l', 'light')
        self.photo_commands = ('p', 'photo', 'take_photo', 'фото', 'сфотографируй')
        self.state_commands = ('s', 'state')
        self.show_last_logs_commands = ('show_last_log', 'log', 'logs')
        self.video_commands = ('video', 'start_video')
        self.volume_commands = ('v', 'звук', 'volume', 'громкость', 'vol')

        self.now = datetime.now()
        self.video_processing = None
        self.video_trigger = False
        self.chat_to_send_video = None
        self.my_stamp_for_video = None
        self.record_qty = None
        self.video_name = None

        while True:
            try:
                self.start_t_bot()
            except Exception as ex:
                logger.error("Exception occurred, waiting 15 secs and rebooting script")
                logger.error(ex)
                sleep(15)

    def send_message(self, last_chat_id, message):
        self.bot.send_message(last_chat_id, message)

    def take_photo(self, chat, param):
        photo_name = f'{self.photo_dir}/{datetime.now().strftime("%d%m%Y-%H%M")}.png'

        if param is None:
            cam = 0
        else:
            if param.isdigit():
                cam = int(param)
            else:
                cam = 0

        photo(photo_name, cam)

        if exists(photo_name):
            self.bot.send_photo(chat, photo_name)
        else:
            self.bot.send_message(chat, f"Ошибка с формированием и отправкой фото")

    @logger.catch()
    def start_t_bot(self):
        new_offset = None
        hour = self.now.hour

        while True:
            self.bot.get_updates(new_offset)

            last_update = self.bot.get_last_update()

            if not last_update:
                continue

            logger.debug(last_update)
            last_update_id = last_update['update_id']

            if 'date' not in last_update['message'].keys():
                new_offset = last_update_id + 1
                continue
            else:
                time_of_update = last_update['message']['date']
            if int(time()) > time_of_update + 5:
                new_offset = last_update_id + 1
                continue

            if 'text' not in last_update['message'].keys():
                new_offset = last_update_id + 1
                continue
            else:
                last_chat_text = last_update['message']['text']

            last_chat_id = last_update['message']['chat']['id']
            last_message_sender_name = last_update['message']['from']['first_name']
            message = last_chat_text.lower()

            if last_chat_id not in self.valid_chats:
                message_to_send = f'unregistered attempt with {last_message_sender_name}, {last_chat_id}, {message}'
                logger.info(message_to_send)
                self.bot.send_message(self.admin_id, message_to_send)
                new_offset = last_update_id + 1
                continue
            # if 'first_name' in last_update['message']['chat']:
            #     last_private_chat_name = last_update['message']['chat']['first_name']
            # else:
            #     last_chat_name = last_update['message']['from']['first_name']

            if self.bot_key in message:
                if message == self.bot_key:
                    self.bot.send_message(last_chat_id, f"Waiting for commends")
                    continue

                cmd = message.split(self.bot_key)[1].split(' ')[0]

                if len(message.split(self.bot_key)[1].split(' ')) > 1:
                    param = message.split(self.bot_key)[1].split(' ')[1]
                    logger.debug(param)
                else:
                    param = None

                msg = ''

                if cmd in self.greetings_commands:
                    msg = send_greetings(last_message_sender_name, hour)
                    # self.bot.send_message(last_chat_id, msg)
                elif cmd in self.renew_ver_git_commands:
                    pass
                elif cmd in self.currency_commands:
                    msg = get_currency(last_chat_id)
                    # self.bot.send_message(last_chat_id, msg)
                elif cmd in self.volume_commands:
                    msg = set_volume(param)
                    # self.bot.send_message(last_chat_id, msg)
                elif cmd in self.photo_commands:
                    self.take_photo(last_chat_id, param)

                elif cmd in self.video_commands:

                    if self.video_trigger is True:
                        self.bot.send_message(last_chat_id, f"Запись проводится")
                        new_offset = last_update_id + 1
                        continue
                    self.bot.send_message(last_chat_id, f"Начинаю запись видео")
                    self.my_stamp_for_video = datetime.now().strftime("%d%m%Y-%H%M")
                    self.video_name = f'{self.video_dir}/{self.my_stamp_for_video}'
                    if param is None:
                        self.record_qty = 1
                    else:
                        if param.isdigit():
                            self.record_qty = int(param)
                        else:
                            self.record_qty = 1
                    try:
                        self.video_processing = Process(target=self.video_thread)
                    except Exception as ex:
                        self.bot.send_message(last_chat_id, f"{ex}")
                        new_offset = last_update_id + 1
                        continue
                    self.video_trigger = True
                    self.chat_to_send_video = last_chat_id
                    self.bot.send_message(last_chat_id, f"Запись начата")
                elif cmd in self.light_commands:
                    self.bot.send_message(last_chat_id, f"Это еще не реализовано")
                if msg:
                    self.bot.send_message(last_chat_id, msg)

            if self.video_trigger:
                if self.video_processing.is_alive() is False:
                    list_of_videos = glob(abspath(f'{self.video_dir}/*'))
                    for video_name in list_of_videos:
                        if video_name.split("/")[-1].split('_')[0] == self.my_stamp_for_video:
                            self.bot.send_video(self.chat_to_send_video, video_name)
                    self.video_trigger = False
            new_offset = last_update_id + 1
            logger.debug(new_offset)

    def video_thread(self):
        v = video.VideoHandler(record_qty=self.record_qty,
                               video_file_name_wout_avi=self.video_name)
        v.run()


if __name__ == '__main__':
    a = MainBot()
