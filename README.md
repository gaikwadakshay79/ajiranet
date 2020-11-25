# SETUP

python -m pip install virtualenv<br />
virtualenv venv<br />

##### if on windows

venv\Scripts\activate.bat<br />

##### if on linux

source venv/bin/activate <br />

python -m pip install -r requirements.txt<br />

## UNIT TESTS

source venv/bin/activate <br />
python -m unittest project.unit_test<br />

## e2e testing

### 1st terminal

source venv/bin/activate<br />
python project/app.py<br />

### 2nd terminal

source venv/bin/activate<br />
python project/e2e.py<br />

# RUN

python project/app.py<br />
