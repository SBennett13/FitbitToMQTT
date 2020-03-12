#!/bin/bash

if  [[ ! -e env ]]; then
    python3 -m venv env;
    source env/bin/activate;
    pip install -r requirements.txt
    wget -P ./env/lib/python3.6/site-packages/gather_keys_oauth2.py https://raw.githubusercontent.com/orcasgit/python-fitbit/master/gather_keys_oauth2.py 
    bash --rcfile ./venvrc
fi
