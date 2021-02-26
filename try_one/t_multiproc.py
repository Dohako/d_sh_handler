import multiprocessing
import time
import t_multiproc_sub
import t_multiproc_sub_2
import loguru


# class MyClass():
#     def __init__(self):
#         first = multiprocessing.Process(target=self.start_test)
#         first.start()
#         second = multiprocessing.Process(target=self.start_test_2)
#         second.start()
#         for i in range(5):
#             time.sleep(1)
#             loguru.logger.info(first.is_alive())
#
#     def start_test(self):
#         loguru.logger.info("Starting first")
#         t_multiproc_sub.Test()
#
#     def start_test_2(self):
#         loguru.logger.info("Starting second")
#         t_multiproc_sub_2.start_me()

def main():
    first = multiprocessing.Process(target=start_test)
    first.start()
    second = multiprocessing.Process(target=start_test_2)
    second.start()
    for i in range(5):
        time.sleep(1)
        loguru.logger.info(first.is_alive())

def start_test():
    loguru.logger.info("Starting first")
    t_multiproc_sub.start_me()

def start_test_2():
    loguru.logger.info("Starting second")
    t_multiproc_sub_2.start_me()

if __name__ == '__main__':
    loguru.logger.add('/home/pi/d_sh_handler/try_one/log.log')
    loguru.logger.info("Started")
    main()