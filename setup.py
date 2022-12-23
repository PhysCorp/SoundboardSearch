# Necessary imports
from distutils.core import setup
import py2exe

# Extra imports
import os
import os.path
import sys
import datetime
import keyboard
import time
import json
import pyautogui
from bs4 import BeautifulSoup
import requests
from playsound import playsound
import subprocess
import win32gui
import win32con
import rich
import rich.traceback
rich.traceback.install()

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [{'script': 'Main.py', 'icon_resources': [(1, 'Icon.ico')], "dest_base" : "SoundboardSearch"}],
    zipfile = None,
    )