# SETUP

python -m pip install virtualenv
virtualenv venv

##### if on windows

venv\Scripts\activate.bat

##### if on linux

source venv/bin/activate

python -m pip install -r requirements.txt

## UNIT TESTS

source venv/bin/activate
python -m unittest project.unit_test

## e2e testing

### 1st terminal

source venv/bin/activate
python project/app.py

### 2nd terminal

source venv/bin/activate
python project/e2e.py

# RUN

python project/app.py
