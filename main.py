from os.path import dirname
from os import system
from time import sleep, time
from multiprocessing import Process
from psutil import virtual_memory, cpu_percent
from dotenv import load_dotenv

from utils.d_sh_h_logger import LogHandler

script_path = dirname(__file__)
logger = LogHandler(script_path=script_path).start()
VERSION = 0.1
logger.info(f"Hello there, d_sh_handler v.{VERSION} is starting")

if not load_dotenv():
    raise FileNotFoundError("There is no .env file")

from t_bot.main_t_bot import MainBot
from rpi_cicd.git_handler import start_git_check


def run_bot():
    """
    Function for chat_bot starting
    previously subprocess.run(['python3', bot_dir]) was used
    """
    logger.info('-'*30)
    logger.info('trying to start bot')
    MainBot(script_path=script_path, logger=logger).start_bot()
    sleep(10)
    logger.info("-"*30)


def run_voice_rec():
    """
    Function for voice recognition starting
    """
    logger.info('-------------------------')
    logger.info('trying to start voice_rec')
    sleep(10)
    logger.info('-------------------------')

def run_git_handler():
    """
    Function will start git handler and if it will falls
    it will mean that new version is uploaded and this can be stoped.
    """
    result = start_git_check(script_path)
    if "updated" in result:
        logger.info("git handler successfully quited")
        return True
    else:
        logger.error(f"git handler quited with {result}")
        return False


class MainClass:
    """
    Main class for all d_sh_handler project.
    It runs all subprocess and keeping them ON.
    In project we have two interfaces to interact with system: chat bot
    and voice recognition system
    """

    @logger.catch()
    def start(self):
        logger.info("trying to start scripts")
        chat_bot_process = Process(target=run_bot)
        chat_bot_process.start()
        logger.info("Started chat bot")
        voice_recognition_process = Process(target=run_voice_rec)
        git_process = Process(target=run_git_handler)
        git_process.start()
        logger.info("Started git checker")
        time_start = int(time())
        checking_time = time_start
        # checking_new_ver_time = time_start
        # checker_process = multiprocessing.Process(target=new_ver_checker)
        # main loop
        while True:
            sleep(3)
            if chat_bot_process.is_alive() is False:
                logger.info("Started chat_bot")
                chat_bot_process = Process(target=run_bot)
                chat_bot_process.start()
                sleep(1)
            if git_process.is_alive() is False:
                logger.info("Git handler was stoped somehow, stoping")
                chat_bot_process.terminate()
                quit()
                
            # if cpu is bigger than 90% or memory is above 80% - need to turn off scripts and reload them
            if int(time()) > checking_time + 5:
                checking_time = int(time())
                # loguru.logger.info(psutil.virtual_memory().percent, psutil.cpu_percent())
                if virtual_memory().percent > 90 or cpu_percent() > 90.0:
                    logger.info(virtual_memory().percent)
                    logger.info(cpu_percent())
                    # logger.info("Shutting down voice_rec")
                    # if voice_recognition_process.is_alive():
                    #     voice_recognition_process.terminate()
                    # sleep(1)
                    # logger.info(virtual_memory().percent)
                    # logger.info(cpu_percent())
                    # logger.info("Shutting down chat_bot")
                    # if chat_bot_process.is_alive():
                    #     chat_bot_process.terminate()
                    # sleep(1)
                    # logger.info(virtual_memory().percent)
                    # logger.info(cpu_percent())
                    # logger.info("Resuming work")

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

    # This two methods should do what?...
    # def set_linux_dirs(self):
    #     # TODO change to dynamic
    #     # main loop scripts dirs
    #     bot_dir = f"/home/pi/d_sh_handler/t_bot/main.py"
    #     bot_ver_dir = f"/home/pi/d_sh_handler/t_bot/ver.txt"
    #     voice_rec_dir = f"/home/pi/d_sh_handler/voice_rec/main.py"
    #     voice_rec_ver_dir = f"/home/pi/d_sh_handler/voice_rec/ver.txt"
    #     # other scripts
    #     image_proc_dir = f"/home/pi/d_sh_handler/image_proc/main.py"
    #     image_proc_ver_dir = f"/home/pi/d_sh_handler/image_proc/ver.txt"
    #     devices_ver_dir = f"/home/pi/d_sh_handler/devices/ver.txt"
    #
    # def set_windows_dirs(self):
    #     bot_dir = f"{dirname(abspath('.'))}\\t_bot\\main.py"
    #     bot_ver_dir = f"{dirname(abspath('.'))}\\t_bot\\ver.txt"
    #     voice_rec_dir = f"{dirname(abspath('.'))}\\voice_rec\\main.py"
    #     voice_rec_ver_dir = f"{dirname(abspath('.'))}\\voice_rec\\ver.txt"
    #     # other scripts
    #     image_proc_dir = f"{dirname(abspath('.'))}\\image_proc\\main.py"
    #     image_proc_ver_dir = f"{dirname(abspath('.'))}\\image_proc\\ver.txt"
    #
    #     devices_ver_dir = f"{dirname(abspath('.'))}\\devices\\ver.txt"


if __name__ == '__main__':
    main_proc = MainClass()
    # main_proc.check_new_ver_once()
    
    while True:
        try:
            main_proc.start()
        except KeyboardInterrupt:
            quit()
        except Exception as ex:
            logger.info(ex)
            system('/home/pi/d_sh_handler/reboot.sh')
    logger.info("Something went not as it is supposed")
