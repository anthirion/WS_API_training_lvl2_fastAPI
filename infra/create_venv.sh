#!/bin/bash

if [ ! -d "/home/anthirion/app/fastapi_venv" ]; then
    python3 -m venv /home/anthirion/app/fastapi_venv
fi
source /home/anthirion/app/fastapi_venv/bin/activate
# pip install -r ~/app/requirements.txt
