from logging import log
from loguru import logger
from telegram.ext import Updater, CommandHandler
from telegram import Update
from dotenv import load_dotenv
from os import getenv
from os.path import getctime
from pathlib import Path
from glob import glob

from telegram.ext.callbackcontext import CallbackContext

from devices.main_audio import change_volume

if not load_dotenv():
    raise FileNotFoundError("There is no .env file")
token = getenv('MY_TOKEN')

ADMINS = ("388863805", "1")


class MainBot:
    def __init__(self, script_path, logger) -> None:
        self.script_path = script_path
        self.logger = logger

    def start_bot(self):
        updater = Updater(token, use_context=True)
        text_to_send_to_admins = f"Бот был запущен!!!"
        updater.bot.send_message(chat_id=ADMINS[0], text=text_to_send_to_admins)
        self.logger.info(text_to_send_to_admins)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('v', self.volume))
        dispatcher.add_handler(CommandHandler('logs', self.get_last_logs))

        updater.start_polling()
        updater.idle()
    
    def volume(self, update:Update, _:CallbackContext):
        chat_id = update.message.chat_id
        volume_percent = update.message.text.split(' ')[1]
        answer = change_volume(volume=volume_percent,logger=logger)
        logger.info(answer)
        update.message.bot.send_message(chat_id=chat_id, text=f"set to {volume_percent}")
    
    def get_last_logs(self, update:Update, _:CallbackContext):
        list_of_files = glob(f'{self.script_path}/logs/*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=getctime)
        # print(latest_file)
        file_name = latest_file
        chat_id = update.message.chat_id
        with open(Path(file_name), 'rb') as file:
            update.bot.send_document(chat_id=chat_id,document=file,filename=file_name)