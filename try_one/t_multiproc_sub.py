import time
import loguru


class Test():
    def __init__(self):
        loguru.logger.add('/home/pi/d_sh_handler/try_one/log.log')
        for i in range(3):
            loguru.logger.info(i)
            time.sleep(1)
