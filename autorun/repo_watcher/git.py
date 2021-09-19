"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

import subprocess

subprocess.run("/home/pi/d_sh_handler/autorun/repo_watcher/git-repo-watcher -d /home/pi/d_sh_handler".split(), 
check=True, text=True)
# subprocess.run("dir", 
# check=True, text=True, shell=True)