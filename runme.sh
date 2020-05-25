#!/bin/bash
git pull
pip3 install -r code/requirements.txt
python3 code/backend.py &&
export FLASK_APP=code/app.py
python3 -m flask run
