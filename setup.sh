#!/bin/bash

if  [[ ! -e env ]]; then
    python3 -m venv env;
    source env/bin/activate;
    pip install -r requirements.txt
    bash --rcfile ./venvrc
    cp gather_keys_oauth.py ./env/lib/python3.6/site-packages/
fi
