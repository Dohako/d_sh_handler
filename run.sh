#!/bin/bash
VENV_DIR="/home/denis/d_sh_handler/venv"

if pgrep -f "python.*main.py" > /dev/null; then
    echo "Found running process of main.py. Killing it..."
    pkill -f "python.*main.py"
else
    echo "No running process of main.py found."
fi

if [ ! -d "$VENV_DIR" ]; then
    cd /home/denis/d_sh_handler
    python -m venv venv
fi
cd /home/denis/d_sh_handler

. ./venv/bin/activate
pip install -r requirements.txt

python main.py