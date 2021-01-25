import os
import time
import loguru
import subprocess
import multiprocessing
import sys
import psutil
import pathlib


def run_bot():
    subprocess.run(['python3', bot_dir])


def run_voice_rec():
    subprocess.run(['python3', voice_rec_dir])


def new_ver_checker():
    pass


def update_voice_rec():
    pass


def update_chat_bot():
    pass


def restart_time():
    pass


def main():
    loguru.logger.info("trying to start scripts")
    chat_bot_process = multiprocessing.Process(target=run_bot)
    voice_recognition_process = multiprocessing.Process(target=run_voice_rec)
    kill_voice_rec = False
    kill_bot_proc = False
    time_start = int(time.time())
    checking_time = time_start
    # checker_process = multiprocessing.Process(target=new_ver_checker)
    while True:
        time.sleep(3)
        if chat_bot_process.is_alive() is False:
            loguru.logger.info("Started chat_bot")
            chat_bot_process = multiprocessing.Process(target=run_bot)
            chat_bot_process.start()
            time.sleep(1)
        if voice_recognition_process.is_alive() is False:
            loguru.logger.info("Started voice_rec")
            voice_recognition_process = multiprocessing.Process(target=run_voice_rec)
            voice_recognition_process.start()
            time.sleep(1)

        # if checker_process.is_alive() is False:
        #     loguru.logger.info("Started checker")
        #     checker_process = multiprocessing.Process(target=new_ver_checker)
        #     checker_process.start()

        # if cpu is bigger than 90% or memory is above 80% - need to turn off scripts and reload them
        if int(time.time()) > checking_time + 5:
            checking_time = int(time.time())
            if psutil.virtual_memory().percent > 80 or psutil.cpu_percent() > 90.0:
                loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
                loguru.logger.info("Shutting down voice_rec")
                if voice_recognition_process.is_alive():
                    voice_recognition_process.terminate()
                time.sleep(1)
                loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
                loguru.logger.info("Shutting down chat_bot")
                if chat_bot_process.is_alive():
                    chat_bot_process.terminate()
                time.sleep(1)
                loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
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
        if new_ver_checker() is True:
            pass
        # every day at 03:00 should be happening reboot of system
        if restart_time() is True:
            pass


if __name__ == '__main__':
    if os.name != 'nt':
        bot_dir = f"{os.path.abspath('.')}/t_bot/main.py"
        voice_rec_dir = f"{os.path.abspath('.')}/voice_rec/main.py"
        image_proc_dir = f"{os.path.abspath('.')}/image_proc/main.py"
    else:
        bot_dir = f"{os.path.dirname(os.path.abspath('.'))}\\t_bot\\main.py"
        voice_rec_dir = f"{os.path.dirname(os.path.abspath('.'))}\\voice_rec\\main.py"
        image_proc_dir = f"{os.path.dirname(os.path.abspath('.'))}\\image_proc\\main.py"
    loguru.logger.add('log.log')
    while True:
        try:
            if main() is False:
                quit()
        except KeyboardInterrupt:
            quit()
