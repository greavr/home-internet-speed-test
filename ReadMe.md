### Python
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
python3 backend.py && python3 -m flask run

deactivate