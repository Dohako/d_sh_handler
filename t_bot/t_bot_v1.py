import sys
import os
if os.name != 'nt':
    import alsaaudio
    # TODO change to dynamic
    sys.path.append(f"/home/pi/d_sh_handler")
import subprocess
import time
from bot_handler import BotHandler
from dotenv import load_dotenv

import datetime
import loguru
import pycbrf
import numpy as np
import cv2
import finam_euro
import take_photo


load_dotenv()
token = os.getenv('MY_TOKEN')
if os.name != 'nt':
    # image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}/image_proc/main.py"
    # photo_dir = f"{os.path.dirname(os.path.abspath('.'))}/photos"
    image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
    photo_dir = f"/home/pi/d_sh_handler/photos"
    if os.path.isdir(photo_dir) is False:
        os.mkdir(photo_dir)
else:
    image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}\\image_proc\\main.py"


bot = BotHandler(token)
greetings_list = ('hello', '/hi', 'qq', 'greetings')
currency_list = ("eur", "usd")
currency_list_correct = ("EUR", "USD")
bot_key = '/'
now = datetime.datetime.now()
admin_id = '388863805'
valid_chats = [388863805, -259505319, -342305508]
admin_commands_list = ['/add_chat_id', '/show_active_chats']
volume_commands = ['звук', 'volume', 'громкость', 'vol', 'v']
photo_commands = ['p', 'photo', 'take_photo', 'фото', 'сфотографируй']
light_commands = ['l']


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    if os.name != 'nt':
        m = alsaaudio.Mixer('Master')  # Headphone
        current_volume = m.getvolume()
        m.setvolume(0)
        loguru.logger.debug(f'current volume is set from {current_volume} to {0}')

    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()

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
        if last_chat_id not in valid_chats:
            new_offset = last_update_id + 1
            continue
        # if 'first_name' in last_update['message']['chat']:
        #     last_private_chat_name = last_update['message']['chat']['first_name']
        # else:
        #     last_chat_name = last_update['message']['from']['first_name']
        last_message_sender_name = last_update['message']['from']['first_name']
        message = last_chat_text.lower()
        if bot_key in message:
            if message == bot_key:
                bot.send_message(last_chat_id, f"Waiting for commends")
                continue
            cmd = message.split(bot_key)[1].split(' ')[0]
            if len(message.split(bot_key)[1].split(' ')) > 1:
                param = message.split(bot_key)[1].split(' ')[1]
                loguru.logger.debug(param)
            else:
                param = None
            if cmd in greetings_list:
                if 6 <= hour < 12:
                    bot.send_message(last_chat_id, f"Доброе утро, {last_message_sender_name}")
                elif 12 <= hour < 18:
                    bot.send_message(last_chat_id, f"Добрый день, {last_message_sender_name}")
                elif 18 <= hour < 23:
                    bot.send_message(last_chat_id, f"Добрый вечер, {last_message_sender_name}")
            elif cmd in currency_list:
                currency = currency_list[currency_list.index(cmd)]
                rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
                currency_name = currency_list_correct[currency_list.index(currency)]
                loguru.logger.debug(currency_name)
                moex_answer = finam_euro.start_t_bot(currency_name)
                bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB CBRF, {moex_answer} RUB Moex")
            # for currency in currency_list:
            #     if currency in last_chat_text.lower():
            #         rates = pycbrf.ExchangeRates(datetime.datetime.now().strftime("%Y-%m-%d"))
            #         currency_name = currency_list_correct[currency_list.index(currency)]
            #         loguru.logger.debug(currency_name)
            #         greet_bot.send_message(last_chat_id, f"1 {currency_name} = {rates[currency_name].value} RUB")

            elif cmd in volume_commands:
                if os.name != 'nt':
                    loguru.logger.debug("Управление звуком зарегистрировано")
                    volume = param
                    if volume.isdigit():
                        int_volume = int(volume)
                        if int_volume > 150:
                            m.setvolume(150)
                            bot.send_message(last_chat_id,
                                             f"Ставлю звук на максимум")
                        elif int_volume < 0:
                            m.setvolume(0)
                            bot.send_message(last_chat_id,
                                             f"Выключаю звук")
                        else:
                            m.setvolume(int_volume)
                            bot.send_message(last_chat_id,
                                             f"Ставлю звук на {int_volume}")
                    else:
                        m.setvolume(0)
                        bot.send_message(last_chat_id,
                                         f"Команда не распознана до конца, выключаю звук")

                else:
                    bot.send_message(last_chat_id, f"Не та ОС")

            elif cmd in photo_commands:
                photo_name = f'{photo_dir}/{datetime.datetime.now().strftime("%d%m%Y-%H%M")}.png'
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
                try:
                    subprocess.run(['python3', image_proc_dir, cam, photo_name, 'photo'])
                except:
                    print('failed on subprocess')
                    take_photo.photo(photo_name, cam)
                if os.path.exists(photo_name):
                    bot.send_photo(last_chat_id, photo_name)
                else:
                    bot.send_message(last_chat_id, f"Ошибка с формированием и отправкой фото")
            elif cmd in light_commands:
                bot.send_message(last_chat_id, f"Это еще не реализовано")

        new_offset = last_update_id + 1
        loguru.logger.debug(new_offset)


if __name__ == '__main__':
    if os.name != 'nt':
        loguru.logger.add('/home/pi/d_sh_handler/log.log')
    else:
        loguru.logger.add('log.log')
    while True:
        try:
            main()
        except KeyboardInterrupt:
            exit()
        except:
            loguru.logger.info("Exception occured, waiting 15 secs and rebooting script")
            time.sleep(15)
