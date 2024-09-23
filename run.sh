#!/bin/bash
VENV_DIR="/home/denis/d_sh_handler/venv"

if [ ! -d "$VENV_DIR" ]; then
    cd /home/denis/d_sh_handler
    python -m venv venv
fi
cd /home/denis/d_sh_handler

. ./venv/bin/activate
pip install -r requirements.txt

python main.py