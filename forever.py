#!/usr/bin/env python3
from subprocess import Popen
import sys, logging, pathlib

while True:
    logging.warning("Restarting bot.py")
    p = Popen([ "./venv/bin/python3", "bot.py"])
    p.wait()

