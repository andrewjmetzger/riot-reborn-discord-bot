#!/usr/bin/env bash 
mkdir -p ./.logs/

./venv/bin/python3 "./forever.py" &> ./.logs/riot_$(date +%F_%T).log

exit