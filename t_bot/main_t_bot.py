from sys import path
from os import name as os_name, getenv, mkdir
from os.path import isdir, dirname, abspath, exists
from subprocess import call
from time import sleep, time
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger
from multiprocessing import Process
from glob import glob

# if os_name != 'nt':
#     # TODO change to dynamic
#     path.append(f"/home/pi/d_sh_handler")

from t_bot.bot_handler import BotHandler
# from t_bot import bot_handler
from utils.courses import scrap_currency_from_page, get_pycbrf_course
from utils.take_photo import photo
from devices import video


class MainBot:

    def __init__(self):
        logger.info("Started bot")
        load_dotenv()
        token = getenv('MY_TOKEN')

        if os_name != 'nt':
            # image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}/image_proc/main.py"
            # photo_dir = f"{os.path.dirname(os.path.abspath('.'))}/photos"
            self.image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
            self.photo_dir = f"/home/pi/d_sh_handler/photos"
            if isdir(self.photo_dir) is False:
                mkdir(self.photo_dir)
            self.video_dir = f"/home/pi/d_sh_handler/videos"
            if isdir(self.video_dir) is False:
                mkdir(self.video_dir)
        else:
            self.image_proc_dir = f"{dirname(abspath('.'))}\\image_proc\\main.py"

        self.bot = BotHandler(token)
        self.greetings_list = ('hello', '/hi', 'qq', 'greetings')
        self.currency_list = ("eur", "usd")
        self.currency_list_correct = ("EUR", "USD")
        self.bot_key = '/'
        self.now = datetime.now()
        self.admin_id = '388863805'
        self.valid_chats = [388863805, -259505319, -342305508]
        self.admin_commands_list = ['/add_chat_id', '/show_active_chats']
        self.volume_commands = ['звук', 'volume', 'громкость', 'vol', 'v']
        self.photo_commands = ['p', 'photo', 'take_photo', 'фото', 'сфотографируй']
        self.video_commands = ['video', 'start_video']
        self.light_commands = ['l']
        self.state_commands = ['s', 'state']
        self.show_last_logs_commands = ['show_last_log']
        self.admin_reboot_device_commands = ['reboot']
        self.renew_ver_git_commands = ['git_renew']
        self.video_processing = None
        self.video_trigger = False
        self.chat_to_send_video = None
        self.my_stamp_for_video = None
        self.record_qty = None
        self.video_name = None

        while True:
            try:
                self.main()
            except KeyboardInterrupt:
                quit()
            except Exception:
                logger.info("Exception occurred, waiting 15 secs and rebooting script")
                sleep(15)

    def send_message(self, last_chat_id):
        self.bot.send_message(last_chat_id, f"_")

    def send_greetings(self, chat, name, time_now):
        if 6 <= time_now < 12:
            self.bot.send_message(chat, f"Доброе утро, {name}")
        elif 12 <= time_now < 18:
            self.bot.send_message(chat, f"Добрый день, {name}")
        elif 18 <= time_now < 23:
            self.bot.send_message(chat, f"Добрый вечер, {name}")

    def main(self):
        new_offset = None
        # today = self.now.day
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
            # try:
            #
            # except KeyError:
            #     new_offset = last_update_id + 1
            #     continue
            last_chat_id = last_update['message']['chat']['id']
            last_message_sender_name = last_update['message']['from']['first_name']
            if last_chat_id not in self.valid_chats:
                message_to_send = f'unregistered attempt with {last_message_sender_name}, {last_chat_id}, ' \
                                  f'{last_chat_text}'
                logger.info(message_to_send)
                self.bot.send_message(self.admin_id, message_to_send)
                new_offset = last_update_id + 1
                continue
            # if 'first_name' in last_update['message']['chat']:
            #     last_private_chat_name = last_update['message']['chat']['first_name']
            # else:
            #     last_chat_name = last_update['message']['from']['first_name']

            message = last_chat_text.lower()
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
                if cmd in self.greetings_list:
                    self.send_greetings(last_chat_id, last_message_sender_name, hour)

                elif cmd in self.renew_ver_git_commands:
                    pass
                elif cmd in self.currency_list:
                    currency = self.currency_list[self.currency_list.index(cmd)]
                    # rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                    currency_name = self.currency_list_correct[self.currency_list.index(currency)]
                    # pycbrf_todays_currency = rates[currency_name].value
                    pycbrf_todays_currency = get_pycbrf_course(currency_name)
                    logger.debug(currency_name)
                    moex_answer = scrap_currency_from_page(currency_name)
                    self.bot.send_message(last_chat_id,
                                          f"1 {currency_name} = {pycbrf_todays_currency} RUB CBRF, "
                                          f"{moex_answer} RUB Moex")
                # for currency in currency_list:
                #     if currency in last_chat_text.lower():
                #         rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                #         currency_name = currency_list_correct[currency_list.index(currency)]
                #         loguru.logger.debug(currency_name)
                #         greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")

                elif cmd in self.volume_commands:
                    if os_name != 'nt':
                        logger.debug("Управление звуком зарегистрировано")
                        volume = param
                        if volume.isdigit():
                            # TODO change way to control sound level
                            int_volume = int(volume)
                            if int_volume > 150:
                                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '100%'])
                                self.bot.send_message(last_chat_id,
                                                      f"Ставлю звук на максимум({audio_answer})")
                            elif int_volume < 0:
                                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
                                self.bot.send_message(last_chat_id,
                                                      f"Выключаю звук({audio_answer})")
                            else:
                                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', f'{int_volume}%'])
                                self.bot.send_message(last_chat_id,
                                                      f"Ставлю звук на {int_volume}({audio_answer})")
                        else:
                            audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
                            self.bot.send_message(last_chat_id,
                                                  f"Команда не распознана до конца, выключаю звук({audio_answer})")

                    else:
                        self.bot.send_message(last_chat_id, f"Не та ОС")

                elif cmd in self.photo_commands:
                    photo_name = f'{self.photo_dir}/{datetime.now().strftime("%d%m%Y-%H%M")}.png'
                    if param is None:
                        cam = 0
                    else:
                        if param.isdigit():
                            cam = int(param)
                        else:
                            cam = 0
                    # TODO make class and refactor
                    photo(photo_name, cam)
                    if exists(photo_name):
                        self.bot.send_photo(last_chat_id, photo_name)
                    else:
                        self.bot.send_message(last_chat_id, f"Ошибка с формированием и отправкой фото")
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
    # while True:
    #     try:
    #
    #     except KeyboardInterrupt:
    #         exit()
    #     except:
    #         loguru.logger.info("Exception occurred, waiting 15 secs and rebooting script")
    #         time.sleep(15)
