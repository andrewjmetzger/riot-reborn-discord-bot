#!/usr/bin/env python3
from subprocess import Popen
import sys, logging, pathlib

while True:
    logging.warning("Restarting bot.py")
    p = Popen([ str(pathlib.Path.home()) + "/Projects/riot-reborn-discord-bot/bot_env/bin/python3", "bot.py"])
    p.wait()

