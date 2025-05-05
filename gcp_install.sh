#!/bin/bash

dest_dir="/home/anthirion/app"

cd "$dest_dir"
python3 -m venv api_venv
source api_venv/bin/activate
pip install -r requirements.txt
fastapi run main.py --port 80 >> logs.txt &