"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

from os import mkdir, name as os_name
from loguru import logger
from datetime import datetime
from os.path import isdir
from subprocess import run


def start_git_check(path):
    if os_name == 'nt':
        # so, on windows i obviously will test some features and don't want to appear any errors 
        # cause of bash scripts
        while True:
            pass

    if isdir(f'{path}/logs') is False:
        mkdir(f'{path}/logs')
    logger.add(f'{path}/logs/log{datetime.now().strftime("%d%m%Y_%H%M")}.log')
    try:
        bash_line = f"{path}/rpi_cicd/git-repo-watcher -d /home/pi/d_sh_handler"
        run(bash_line.split(), check=True, text=True)
    except Exception as ex:
        logger.info("*"*100)
        logger.info(ex)
        if "10" in str(ex):
            # I changed bash script a little from it start status and now it sends error №10, if new version 
            # was installed, so here I'm trying to catch it.
            # TODO think of another way to work with new version.
            return "repo is updated"
        # of course, if error is connected to anything else - I want to know it, so raise
        raise
