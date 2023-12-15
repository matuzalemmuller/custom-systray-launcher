#!/bin/bash

if [ ! -d env ]; then
    python3 -m virtualenv env
    source env/local/bin/activate
    pip3 install -r requirements.txt
else
    source env/local/bin/activate
fi

python3 systray.py
