from datetime import datetime
import os
import time
import requests
from time import sleep, time
from multiprocessing import Process
from psutil import virtual_memory, cpu_percent


# Replace these with your bot's API token and your chat ID
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
TG_ADMIN_ID = os.getenv('TG_ADMIN_ID')
if not BOT_API_TOKEN or not TG_ADMIN_ID:
    raise Exception("no env vars")
MESSAGE = 'Hello, Denis! This is a test message from your bot.'

def send_debug_telegram_message(message: str) -> None:
    
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    data: dict[str, str] = {
        'chat_id': TG_ADMIN_ID if TG_ADMIN_ID else '',
        'text': message
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def get_raw_updates(bot_token: str):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        print(updates)
    else:
        print(f"Failed to get updates. Status code: {response.status_code}, Response: {response.text}")



def run_bot():
    """
    Function for chat_bot starting
    previously subprocess.run(['python3', bot_dir]) was used
    """
    from t_bot.main_t_bot import MainBot
    send_debug_telegram_message('trying to start tg bot')
    MainBot().start_bot()
    sleep(10)


class MainClass:
    """
    Main class for all d_sh_handler project.
    It runs all subprocess and keeping them ON.
    In project we have two interfaces to interact with system: chat bot
    and voice recognition system
    """

    def start(self):
        chat_bot_process = Process(target=run_bot)
        chat_bot_process.start()
        # voice_recognition_process = Process(target=run_voice_rec)
        # git_process = Process(target=run_git_handler)
        # git_process.start()
        time_start = int(time())
        checking_time = time_start
        # checking_new_ver_time = time_start
        # checker_process = multiprocessing.Process(target=new_ver_checker)
        # main loop
        while True:
            sleep(3)
            if chat_bot_process.is_alive() is False:
                # logger.info("Started chat_bot")
                chat_bot_process = Process(target=run_bot)
                chat_bot_process.start()
                sleep(1)
            # if git_process.is_alive() is False:
            #     logger.info("Git handler was stoped somehow, stoping")
            #     chat_bot_process.terminate()
            #     quit()
                
            # if cpu is bigger than 90% or memory is above 80% - need to turn off scripts and reload them
            if int(time()) > checking_time + 120:
                checking_time = int(time())
                if virtual_memory().percent > 90 or cpu_percent() > 90.0:
                    send_debug_telegram_message(f"VRAM IS {virtual_memory().percent}")
                    send_debug_telegram_message(f"CPU IS {cpu_percent()}")

if __name__ == "__main__":
    send_debug_telegram_message(
        f"Hello! Main program has started, server time is: {datetime.now().isoformat()}"
    )
    main_proc = MainClass()
    # main_proc.check_new_ver_once()
    
    while True:
        try:
            main_proc.start()
        except KeyboardInterrupt:
            sleep(60)
            quit()
        except Exception as ex:
            send_debug_telegram_message(str(ex))
            sleep(60)
            # system('/home/pi/d_sh_handler/reboot.sh')

