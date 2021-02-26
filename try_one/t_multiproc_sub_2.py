import time
import loguru


class Test2():
    def __init__(self):
        loguru.logger.add('/home/pi/d_sh_handler/try_one/log.log')
        for i in [10,9,8]:
            loguru.logger.info(i)
            time.sleep(1)
