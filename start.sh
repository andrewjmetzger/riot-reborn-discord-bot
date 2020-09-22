#!/usr/bin/env bash 
mkdir ./.logs/
./bot_env/bin/python3 "forever.py" &> ./.logs/riot_$(date +%F_%T).log
exit