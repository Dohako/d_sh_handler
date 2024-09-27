from datetime import datetime
import os
from telegram.ext import CommandHandler, ApplicationBuilder
from telegram import Update

from os import getenv, mkdir
from os.path import isdir
# from pathlib import Path
# from glob import glob
# from datetime import datetime
from subprocess import run

from telegram.ext._callbackcontext import CallbackContext

# from devices.main_audio import change_volume
# from devices.main_audio import AudioHandler
from devices.camera_handler import take_photo

# if not load_dotenv('../.env'):
#     raise FileNotFoundError("There is no .env file")
TOKEN = getenv('BOT_API_TOKEN')
ADMINS = getenv("TG_ADMIN_ID").replace(' ', '').split(",")
TRUST_ID = getenv("TG_ADMIN_ID").replace(' ', '').split(",")
PHOTO_DIR = "/home/denis/d_sh_handler/photos"
VIDEO_DIR = "/home/denis/d_sh_handler/videos"

if isdir(PHOTO_DIR) is False:
    mkdir(PHOTO_DIR)
if isdir(VIDEO_DIR) is False:
    mkdir(VIDEO_DIR)

def normalize_params(text:str) -> list:
    """
    need to create standard function to normalize parametrs
    But first need to understand what params there could be
    """
    result = list()
    # for default value list of one 0 will be returned
    result.append('0')
    if ' ' in text:
        if '/' in text:
            params = text.split(' ')[1:]
            for param in params:
                pass # stoped creating here cause of different possible value types...
            result = params
    elif "_" in text:
        params = text.split('_')[1:]
        result = params
    return result

def is_admin(func):
    """
    There obviously is functions/methods that should not be available for all users
    """
    def wrap(_, update: Update, callback: CallbackContext):
        if update.message:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        if str(chat_id) in ADMINS:
            val = func(_,update,callback)
        else:
            val = 0
        return val
    return wrap

# def is_trust(func):
#     def wrap(_, update: Update, callback: CallbackContext):
#         if update.message:
#             chat_id = update.message.chat_id
#         else:
#             chat_id = update.callback_query.message.chat_id
#         if str(chat_id) in TRUST_ID:
#             val = func(_,update,callback)
#         else:
#             val = 0
#         return val
#     return wrap

class MainBot:

    def start_bot(self):
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("c", self.run_shell_command))
        app.add_handler(CommandHandler("p", self.get_photo))

        app.run_polling()
        # updater = Updater(TOKEN, use_context=True)
        # text_to_send_to_admins = f"Бот был запущен!!!"
        # updater.bot.send_message(chat_id=ADMINS[0], text=text_to_send_to_admins)

        # dispatcher = updater.dispatcher

        # dispatcher.add_handler(CommandHandler('v', self.set_volume))
        # dispatcher.add_handler(CommandHandler('logs', self.get_last_logs))
        # dispatcher.add_handler(CommandHandler("c", self.run_shell_command))

        # # TODO find way to make bellow through regex
        # dispatcher.add_handler(CommandHandler("p", self.get_photo))
        # dispatcher.add_handler(CommandHandler("p_1", self.get_photo))


        # updater.start_polling()
        # updater.idle()

    @is_admin
    async def run_shell_command(self, update:Update, _:CallbackContext) -> None:
        """
        test with shell commands in one line
        """
        assert update.message
        chat_id = update.message.chat_id
        text = update.message.text
        params = normalize_params(text)
        print(params)
        try:
            result = run(params, check=True, text=True, capture_output=True)
        
            message = f"out:\n{result.stdout}\nerror:\n{result.stderr}."
        except Exception as ex: # base exception bad, but i want to see all exceptions
            message = str(ex)
        await update.message._bot.send_message(chat_id=chat_id, text=message)

    @is_admin
    async def get_photo(self, update:Update, _:CallbackContext) -> None:
        assert update.message
        assert update.message._bot
        chat_id = update.message.chat_id
        photo_name = f'{PHOTO_DIR}/{datetime.now().strftime("%d%m%Y-%H%M")}.png'
        
        # text = update.message.text
        # params = list()
        # params = normalize_params(text)
        cam_number = 0
        # if cam_number.isdigit():
        #     cam_number = int(cam_number)
        #     if cam_number > 1 or cam_number < 0:
        #         cam_number = 0
        # else:
        #     cam_number = 0
        take_photo(cam_number, photo_name)

        if os.path.exists(photo_name):
            with open(photo_name, 'rb') as photo:
                await update.message._bot.send_photo(chat_id=chat_id, photo=photo)
        else:
            await update.message._bot.send_message(chat_id=chat_id, text=f"Ошибка с формированием и отправкой фото")
    
    # @is_trust
    # def set_volume(self, update:Update, _:CallbackContext):
    #     chat_id = update.message.chat_id
    #     volume_percent = update.message.text.split(' ')[1]
    #     # answer = change_volume(volume=volume_percent,logger=logger)
    #     audio = AudioHandler().change_volume_alsa(volume_percent)
    #     update.message.bot.send_message(chat_id=chat_id, text=f"set to {volume_percent}")
    
    # @is_admin
    # def get_last_logs(self, update:Update, _:CallbackContext):
    #     list_of_files = glob(f'{self.script_path}/logs/*')  # * means all if need specific format then *.csv
    #     latest_file = max(list_of_files, key=getctime)
    #     # print(latest_file)
    #     file_name = latest_file
    #     chat_id = update.message.chat_id
    #     with open(Path(file_name), 'rb') as file:
    #         update.bot.send_document(chat_id=chat_id,document=file,filename=file_name)