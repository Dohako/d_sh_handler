import sys
import os
if os.name != 'nt':
    import alsaaudio

    # TODO change to dynamic
    sys.path.append(f"/home/pi/d_sh_handler")
import subprocess
import time
import bot_handler
from dotenv import load_dotenv
import datetime
import loguru
import pycbrf
import numpy as np
import cv2
import finam_euro
import take_photo


class MainBot:

    def __init__(self):
        if os.name != 'nt':
            loguru.logger.add('/home/pi/d_sh_handler/log.log')
        else:
            loguru.logger.add('log.log')

        load_dotenv()
        token = os.getenv('MY_TOKEN')
        if os.name != 'nt':
            # image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}/image_proc/main.py"
            # photo_dir = f"{os.path.dirname(os.path.abspath('.'))}/photos"
            self.image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
            self.photo_dir = f"/home/pi/d_sh_handler/photos"
            if os.path.isdir(self.photo_dir) is False:
                os.mkdir(self.photo_dir)
        else:
            self.image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}\\image_proc\\main.py"

        self.bot = bot_handler.BotHandler(token)
        self.greetings_list = ('hello', '/hi', 'qq', 'greetings')
        self.currency_list = ("eur", "usd")
        self.currency_list_correct = ("EUR", "USD")
        self.bot_key = '/'
        self.now = datetime.datetime.now()
        self.admin_id = '388863805'
        self.valid_chats = [388863805, -259505319, -342305508]
        self.admin_commands_list = ['/add_chat_id', '/show_active_chats']
        self.volume_commands = ['звук', 'volume', 'громкость', 'vol', 'v']
        self.photo_commands = ['p', 'photo', 'take_photo', 'фото', 'сфотографируй']
        self.light_commands = ['l']

        while True:
            try:
                self.main()
            except KeyboardInterrupt:
                quit()
            except Exception as ex:
                loguru.logger.error(ex)
                loguru.logger.info("Exception occurred, waiting 15 secs and rebooting script")
                time.sleep(15)

    def main(self):
        new_offset = None
        today = self.now.day
        hour = self.now.hour

        if os.name != 'nt':
            try:
                m = alsaaudio.Mixer('Master')  # Headphone
            except Exception as ex:
                loguru.logger.error(ex)
                loguru.logger.info(alsaaudio.mixers())
                quit()
            current_volume = m.getvolume()
            m.setvolume(0)
            loguru.logger.debug(f'current volume is set from {current_volume} to {0}')
        else:
            m = None

        while True:
            self.bot.get_updates(new_offset)

            last_update = self.bot.get_last_update()

            if not last_update:
                continue

            loguru.logger.debug(last_update)
            last_update_id = last_update['update_id']

            if 'date' not in last_update['message'].keys():
                new_offset = last_update_id + 1
                continue
            else:
                time_of_update = last_update['message']['date']
            if int(time.time()) > time_of_update + 5:
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
            if last_chat_id not in self.valid_chats:
                new_offset = last_update_id + 1
                continue
            # if 'first_name' in last_update['message']['chat']:
            #     last_private_chat_name = last_update['message']['chat']['first_name']
            # else:
            #     last_chat_name = last_update['message']['from']['first_name']
            last_message_sender_name = last_update['message']['from']['first_name']
            message = last_chat_text.lower()
            if self.bot_key in message:
                if message == self.bot_key:
                    self.bot.send_message(last_chat_id, f"Waiting for commends")
                    continue
                cmd = message.split(self.bot_key)[1].split(' ')[0]
                if len(message.split(self.bot_key)[1].split(' ')) > 1:
                    param = message.split(self.bot_key)[1].split(' ')[1]
                    loguru.logger.debug(param)
                else:
                    param = None
                if cmd in self.greetings_list:
                    if 6 <= hour < 12:
                        self.bot.send_message(last_chat_id, f"Доброе утро, {last_message_sender_name}")
                    elif 12 <= hour < 18:
                        self.bot.send_message(last_chat_id, f"Добрый день, {last_message_sender_name}")
                    elif 18 <= hour < 23:
                        self.bot.send_message(last_chat_id, f"Добрый вечер, {last_message_sender_name}")
                elif cmd in self.currency_list:
                    currency = self.currency_list[self.currency_list.index(cmd)]
                    rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                    currency_name = self.currency_list_correct[self.currency_list.index(currency)]
                    loguru.logger.debug(currency_name)
                    moex_answer = finam_euro.main(currency_name)
                    self.bot.send_message(last_chat_id,
                                          f"1 {currency_name} = {rates[currency_name].value} RUB CBRF, "
                                          f"{moex_answer} RUB Moex")
                # for currency in currency_list:
                #     if currency in last_chat_text.lower():
                #         rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                #         currency_name = currency_list_correct[currency_list.index(currency)]
                #         loguru.logger.debug(currency_name)
                #         greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")

                elif cmd in self.volume_commands:
                    if os.name != 'nt':
                        loguru.logger.debug("Управление звуком зарегистрировано")
                        volume = param
                        if volume.isdigit():
                            int_volume = int(volume)
                            if int_volume > 150:
                                m.setvolume(150)
                                self.bot.send_message(last_chat_id,
                                                      f"Ставлю звук на максимум")
                            elif int_volume < 0:
                                m.setvolume(0)
                                self.bot.send_message(last_chat_id,
                                                      f"Выключаю звук")
                            else:
                                m.setvolume(int_volume)
                                self.bot.send_message(last_chat_id,
                                                      f"Ставлю звук на {int_volume}")
                        else:
                            m.setvolume(0)
                            self.bot.send_message(last_chat_id,
                                                  f"Команда не распознана до конца, выключаю звук")

                    else:
                        self.bot.send_message(last_chat_id, f"Не та ОС")

                elif cmd in self.photo_commands:
                    photo_name = f'{self.photo_dir}/{datetime.datetime.now().strftime("%d%m%Y-%H%M")}.png'
                    # subprocess.call(f'fswebcam -q -r 1280x720 {photo_name}', shell=True)
                    if param is None:
                        cam = 0
                    else:
                        if param.isdigit():
                            cam = int(param)
                        else:
                            cam = 0
                    # cap = cv2.VideoCapture(cam)
                    # ret,frame = cap.read()
                    # cv2.imshow('img1', frame)
                    # cv2.imwrite(photo_name, frame)
                    # cv2.destroyAllWindows()
                    # cap.release()
                    # TODO make class and refactor
                    # try:
                    #     subprocess.run(['python3', self.image_proc_dir, cam, photo_name, 'photo'])
                    # except:
                    #     print('failed on subprocess')
                    take_photo.photo(photo_name, cam)
                    if os.path.exists(photo_name):
                        self.bot.send_photo(last_chat_id, photo_name)
                    else:
                        self.bot.send_message(last_chat_id, f"Ошибка с формированием и отправкой фото")
                elif cmd in self.light_commands:
                    self.bot.send_message(last_chat_id, f"Это еще не реализовано")

            new_offset = last_update_id + 1
            loguru.logger.debug(new_offset)


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
