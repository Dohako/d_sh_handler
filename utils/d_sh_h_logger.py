from loguru import logger
from sys import path as s_path
from os.path import isdir
from os import mkdir
from datetime import datetime

import loguru

class LogHandler():

    def __init__(self, script_path) -> None:
        self.script_path = script_path

    def start(self) -> logger:
        if not self.script_path or self.script_path == '/':
            self.script_path = s_path[0]
            if not self.script_path or self.script_path == '/':
                self.script_path = '/home/pi/d_sh_handler'
        if isdir(f'{self.script_path}/logs') is False:
            mkdir(f'{self.script_path}/logs')
        logger.add(f'{self.script_path}/logs/log{datetime.now().strftime("%d%m%Y_%H%M")}.log')

        return logger
