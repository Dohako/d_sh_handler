"""
This script will check git updates every N time and if there is some, then it will pull it and quit
"""

import subprocess
try:
    results = subprocess.run("/home/pi/d_sh_handler/rpi_cicd/git-repo-watcher -d /home/pi/d_sh_handler".split(), check=True, text=True)
except Exception as ex:
    print(ex)
print(results.stdout)
# subprocess.run("dir", 
# check=True, text=True, shell=True)