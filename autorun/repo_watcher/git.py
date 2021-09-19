"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

import subprocess

subprocess.run("sudo /home/pi/d_sh_handler/autorun/repo_watcher/git-repo-watcher -d /home/pi/d_sh_handler", 
check=True, text=True, shell=True)
# subprocess.run("dir", 
# check=True, text=True, shell=True)