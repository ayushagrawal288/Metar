Metar
===========

Problem Statement
-----------------
Decode Metar codes

## Heroku link -> https://metarapp.herokuapp.com/


Getting Started
---------------

- Change directory into your newly created project.

    cd metar/

- Create a Python virtual environment.

    virtualenv -p python3 venv
    source venv/bin/activate

- Upgrade packaging tools.

    pip install -r requirements.txt

- Run your project.

    python manage.py runserver

Endpoints
---------
Book:   
- Ping(get):
    /metar/ping

- Info(get):
    /metar/info?scode=****&nocache=0/1

