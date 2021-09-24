from telegram import Updater
from dotenv import load_dotenv
from os import getenv

from utils.d_sh_h_logger import LogHandler

if not load_dotenv():
    raise FileNotFoundError("There is no .env file")
token = getenv('MY_TOKEN')

ADMINS = ("388863805", "1")

class MainBot:
    def __init__(self, script_path) -> None:
        self.logger = LogHandler(script_path).start()
        updater = Updater(token, use_context=True)
        text_to_send_to_admins = f"Бот был запущен"
        updater.bot.send_message(chat_id=ADMINS[0], text=text_to_send_to_admins)
        self.logger.info(text_to_send_to_admins)
        while True:
            pass