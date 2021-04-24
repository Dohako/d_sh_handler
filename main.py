from loguru import logger
from os import name, system, mkdir
from os.path import abspath, dirname, isdir
from time import sleep, time
from multiprocessing import Process
from psutil import virtual_memory, cpu_percent
from datetime import datetime

from t_bot.main_t_bot import MainBot


class MainClass:
    """
    Main class for all d_sh_handler project.
    It runs all subprocess and keeping them ON.
    In project we have two interfaces to interact with system: chat bot
    and voice recognition system
    """

    def run_bot(self):
        """
        Method for chat_bot starting
        """
        logger.info('-------------------------')
        logger.info('trying to start bot')
        # subprocess.run(['python3', bot_dir])
        MainBot()
        logger.info('-------------------------')

    def run_voice_rec(self):
        """
        Method for voice recognition starting
        """
        logger.info('-------------------------')
        logger.info('trying to start voice_rec')
        # subprocess.run(['python3', voice_rec_dir])
        sleep(10)
        logger.info('-------------------------')

    def new_ver_checker(self):
        pass

    def update_all(self):
        pass

    def update_voice_rec(self):
        pass

    def update_chat_bot(self):
        pass

    def restart_time(self):
        pass

    def take_versions(self):
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

    @logger.catch()
    def start(self):
        logger.info("trying to start scripts")
        chat_bot_process = Process(target=self.run_bot)
        voice_recognition_process = Process(target=self.run_voice_rec)
        # check current versions for all components
        self.take_versions()
        kill_voice_rec = False
        kill_bot_proc = False
        # timers
        time_start = int(time())
        checking_time = time_start
        checking_new_ver_time = time_start
        # checker_process = multiprocessing.Process(target=new_ver_checker)
        # main loop
        while True:
            sleep(3)
            if chat_bot_process.is_alive() is False:
                logger.info("Started chat_bot")
                chat_bot_process = Process(target=self.run_bot)
                chat_bot_process.start()
                sleep(1)
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
            if int(time()) > checking_time + 5:
                checking_time = int(time())
                # loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
                if virtual_memory().percent > 90 or cpu_percent() > 90.0:
                    logger.info(virtual_memory().percent)
                    logger.info(cpu_percent())
                    logger.info("Shutting down voice_rec")
                    if voice_recognition_process.is_alive():
                        voice_recognition_process.terminate()
                    sleep(1)
                    logger.info(virtual_memory().percent)
                    logger.info(cpu_percent())
                    logger.info("Shutting down chat_bot")
                    if chat_bot_process.is_alive():
                        chat_bot_process.terminate()
                    sleep(1)
                    logger.info(virtual_memory().percent)
                    logger.info(cpu_percent())
                    logger.info("Resuming work")

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
            if int(time()) > checking_time + 60:
                checking_time = int(time())
                if self.new_ver_checker() is True:
                    pass
            # every day at 03:00 should be happening reboot of system
            if self.restart_time() is True:
                pass

    # This two methods should do what?...
    def set_linux_dirs(self):
        # TODO change to dynamic
        # main loop scripts dirs
        bot_dir = f"/home/pi/d_sh_handler/t_bot/main.py"
        bot_ver_dir = f"/home/pi/d_sh_handler/t_bot/ver.txt"
        voice_rec_dir = f"/home/pi/d_sh_handler/voice_rec/main.py"
        voice_rec_ver_dir = f"/home/pi/d_sh_handler/voice_rec/ver.txt"
        # other scripts
        image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
        image_proc_ver_dir = f"/home/pi/d_sh_handler/image_proc/ver.txt"
        devices_ver_dir = f"/home/pi/d_sh_handler/devices/ver.txt"

    def set_windows_dirs(self):
        bot_dir = f"{dirname(abspath('.'))}\\t_bot\\main.py"
        bot_ver_dir = f"{dirname(abspath('.'))}\\t_bot\\ver.txt"
        voice_rec_dir = f"{dirname(abspath('.'))}\\voice_rec\\main.py"
        voice_rec_ver_dir = f"{dirname(abspath('.'))}\\voice_rec\\ver.txt"
        # other scripts
        image_proc_dir = f"{dirname(abspath('.'))}\\image_proc\\main.py"
        image_proc_ver_dir = f"{dirname(abspath('.'))}\\image_proc\\ver.txt"

        devices_ver_dir = f"{dirname(abspath('.'))}\\devices\\ver.txt"


if __name__ == '__main__':
    # nt for linux
    logger.add('/home/pi/d_sh_handler/log.log')
    path = dirname(__file__)
    logger.info(path)
    logger.info(isdir(f'{path}/logs'))
    if isdir(f'{path}/logs') is False:
        mkdir(f'{path}/logs')
    logger.info("Done")
    # if name != 'nt':
    #     logger.add(f'logs/log{}.log')
    # else:

    logger.add(f'{path}/logs/log{datetime.now().strftime("%d%m%Y_%H%M")}.log')
    logger.info('Started main script')
    logger.info("Done new log")
    quit()
    main_proc = MainClass()
    while True:
        try:
            main_proc.start()
        except KeyboardInterrupt:
            quit()
        except Exception:
            system('/home/pi/d_sh_handler/reboot.sh')
