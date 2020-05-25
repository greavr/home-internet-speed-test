#!/bin/bash
git pull
python3 pip3 install -r code/requirementes.txt
python3 code/background.py &&
export FLASK_APP=code/app.py
python3 -m flask run
