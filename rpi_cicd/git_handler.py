"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

from os import name
import subprocess

def main():
    try:
        subprocess.run("/home/pi/d_sh_handler/rpi_cicd/git-repo-watcher -d /home/pi/d_sh_handler".split(), check=True, text=True)
    except Exception as ex:
        print("*"*100)
        print(ex)
        if "10" in ex:
            return "repo is updated"
        raise
# subprocess.run("dir", 
# check=True, text=True, shell=True)

if __name__ == '__main__':
    main()