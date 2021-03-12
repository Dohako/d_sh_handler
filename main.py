import loguru
import os
if os.name != 'nt':
    loguru.logger.add('/home/pi/d_sh_handler/log.log')
    loguru.logger.info("Hello there")
else:
    loguru.logger.add('log.log')

import time
import subprocess
import multiprocessing
import sys
import psutil
import pathlib
import bs4
# if os.name != 'nt':
#     # TODO change to dynamic
#     sys.path.append("/home/pi/d_sh_handler")
#     sys.path.append("/home/pi/d_sh_handler/t_bot")
loguru.logger.info("Importing main_t_bot")
try:
    from t_bot import main_t_bot
except Exception as ex:
    loguru.logger.error(ex)
    quit()
loguru.logger.info("Imported")

ver_chat_bot: str = ''
ver_voice_rec: str = ''
ver_image_proc: str = ''
ver_devices: str = ''


def run_bot():
    loguru.logger.info('-------------------------')
    loguru.logger.info('trying to start bot')
    # subprocess.run(['python3', bot_dir])
    a = main_t_bot.MainBot()

    loguru.logger.info('-------------------------')


def run_voice_rec():
    loguru.logger.info('-------------------------')
    loguru.logger.info('trying to start voice_rec')
    # subprocess.run(['python3', voice_rec_dir])
    time.sleep(10)
    loguru.logger.info('-------------------------')


def new_ver_checker():
    pass


def update_all():
    pass


def update_voice_rec():
    pass


def update_chat_bot():
    pass


def restart_time():
    pass


def take_versions():
    pass
    #
    # global ver_chat_bot, ver_voice_rec, ver_image_proc, ver_devices
    # ver = open(bot_ver_dir, 'r')
    # ver_chat_bot = ver.read()
    #
    # ver = open(voice_rec_ver_dir, 'r')
    # ver_voice_rec = ver.read()
    #
    # ver = open(image_proc_ver_dir, 'r')
    # ver_image_proc = ver.read()
    #
    # ver = open(devices_ver_dir, 'r')
    # ver_devices = ver.read()


@loguru.logger.catch()
def main():
    loguru.logger.info("trying to start scripts")
    chat_bot_process = multiprocessing.Process(target=run_bot)
    voice_recognition_process = multiprocessing.Process(target=run_voice_rec)
    # check current versions for all components
    take_versions()
    kill_voice_rec = False
    kill_bot_proc = False
    # timers
    time_start = int(time.time())
    checking_time = time_start
    checking_new_ver_time = time_start
    # checker_process = multiprocessing.Process(target=new_ver_checker)
    # main loop
    while True:
        time.sleep(3)
        if chat_bot_process.is_alive() is False:
            loguru.logger.info("Started chat_bot")
            chat_bot_process = multiprocessing.Process(target=run_bot)
            chat_bot_process.start()
            time.sleep(1)
        # TODO restore voice_rec
        # if voice_recognition_process.is_alive() is False:
        #     pass
        #
        #     loguru.logger.info("Started voice_rec")
        #     voice_recognition_process = multiprocessing.Process(target=run_voice_rec)
        #     loguru.logger.info(voice_recognition_process.is_alive())
        #     voice_recognition_process.start()
        #     time.sleep(1)

        # if checker_process.is_alive() is False:
        #     loguru.logger.info("Started checker")
        #     checker_process = multiprocessing.Process(target=new_ver_checker)
        #     checker_process.start()

        # if cpu is bigger than 90% or memory is above 80% - need to turn off scripts and reload them
        if int(time.time()) > checking_time + 5:
            checking_time = int(time.time())
            # loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
            if psutil.virtual_memory().percent > 90 or psutil.cpu_percent() > 90.0:
                loguru.logger.info(psutil.virtual_memory().percent)
                loguru.logger.info(psutil.cpu_percent())
                loguru.logger.info("Shutting down voice_rec")
                if voice_recognition_process.is_alive():
                    voice_recognition_process.terminate()
                time.sleep(1)
                loguru.logger.info(psutil.virtual_memory().percent)
                loguru.logger.info(psutil.cpu_percent())
                loguru.logger.info("Shutting down chat_bot")
                if chat_bot_process.is_alive():
                    chat_bot_process.terminate()
                time.sleep(1)
                loguru.logger.info(psutil.virtual_memory().percent)
                loguru.logger.info(psutil.cpu_percent())
                loguru.logger.info("Resuming work")

        # if kill_voice_rec is True:
        #     if voice_recognition_process.is_alive():
        #         voice_recognition_process.terminate()
        #     kill_voice_rec = False
        #
        # if kill_bot_proc is True:
        #     if chat_bot_process.is_alive():
        #         chat_bot_process.terminate()
        #     kill_bot_proc = False
        # every 1 minute should happen version checking
        if int(time.time()) > checking_time + 60:
            checking_time = int(time.time())
            if new_ver_checker() is True:
                pass
        # every day at 03:00 should be happening reboot of system
        if restart_time() is True:
            pass


if __name__ == '__main__':
    # nt for linux
    if os.name != 'nt':
        # main loop scripts dirs
        # bot_dir = f"{os.path.abspath('.')}/t_bot/main.py"
        # bot_ver_dir = f"{os.path.abspath('.')}/t_bot/ver.txt"
        # voice_rec_dir = f"{os.path.abspath('.')}/voice_rec/main.py"
        # voice_rec_ver_dir = f"{os.path.abspath('.')}/voice_rec/ver.txt"
        # # other scripts
        # image_proc_dir = f"{os.path.abspath('.')}/image_proc/main.py"
        # image_proc_ver_dir = f"{os.path.abspath('.')}/image_proc/ver.txt"
        #
        # devices_ver_dir = f"{os.path.abspath('.')}/devices/ver.txt"
        bot_dir = f"/home/pi/d_sh_handler/t_bot/main.py"
        bot_ver_dir = f"/home/pi/d_sh_handler/t_bot/ver.txt"
        voice_rec_dir = f"/home/pi/d_sh_handler/voice_rec/main.py"
        voice_rec_ver_dir = f"/home/pi/d_sh_handler/voice_rec/ver.txt"
        # other scripts
        image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
        image_proc_ver_dir = f"/home/pi/d_sh_handler/image_proc/ver.txt"

        devices_ver_dir = f"/home/pi/d_sh_handler/devices/ver.txt"
        # loguru.logger.add('/home/pi/d_sh_handler/log.log')
    else:
        # main loop scripts dirs
        bot_dir = f"{os.path.dirname(os.path.abspath('.'))}\\t_bot\\main.py"
        bot_ver_dir = f"{os.path.dirname(os.path.abspath('.'))}\\t_bot\\ver.txt"
        voice_rec_dir = f"{os.path.dirname(os.path.abspath('.'))}\\voice_rec\\main.py"
        voice_rec_ver_dir = f"{os.path.dirname(os.path.abspath('.'))}\\voice_rec\\ver.txt"
        # other scripts
        image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}\\image_proc\\main.py"
        image_proc_ver_dir = f"{os.path.dirname(os.path.abspath('.'))}\\image_proc\\ver.txt"

        devices_ver_dir = f"{os.path.dirname(os.path.abspath('.'))}\\devices\\ver.txt"

    loguru.logger.info('Started main script')
    while True:
        try:
            if main() is False:
                quit()
        except KeyboardInterrupt:
            quit()
        except:
            os.system('/home/pi/d_sh_handler/reboot.sh')
