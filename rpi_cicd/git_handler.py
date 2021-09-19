"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

from os import mkdir
from loguru import logger
from datetime import datetime
from os.path import dirname, isdir
import subprocess

def main():
    path = dirname(__file__)
    if isdir(f'{path}/logs') is False:
        mkdir(f'{path}/logs')
    logger.add(f'{path}/logs/log{datetime.now().strftime("%d%m%Y_%H%M")}.log')
    try:
        subprocess.run("/home/pi/d_sh_handler/rpi_cicd/git-repo-watcher -d /home/pi/d_sh_handler".split(), check=True, text=True)
    except Exception as ex:
        logger.info("*"*100)
        logger.info(ex)
        if "10" in str(ex):
            return "repo is updated"
        raise
# subprocess.run("dir", 
# check=True, text=True, shell=True)

if __name__ == '__main__':
    main()