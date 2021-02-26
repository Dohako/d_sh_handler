import multiprocessing
import time
import t_multiproc_sub
import t_multiproc_sub_2


class MyClass():
    def __init__(self):
        first = multiprocessing.Process(target=self.start_test)
        first.start()
        second = multiprocessing.Process(target=self.start_test_2)
        second.start()
        for i in range(5):
            time.sleep(1)
            print(first.is_alive())

    def start_test(self):
        t_multiproc_sub.Test()

    def start_test_2(self):
        t_multiproc_sub_2.Test2()


if __name__ == '__main__':
    a = MyClass()