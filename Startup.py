from cgi import test
import Settings
import os
import re
import json 
import asyncio
import time
import shlex
from ast import literal_eval
from io import StringIO
import platform

# print(Settings.token)

if Settings.auto_update:
    print("Updating imports")
    os.system('python -m pip install -U "pyyaml"')    
    os.system('python -m pip install -U "Wavelink"')
    os.system('python -m pip install -U "discord.py[voice]"')

    print("Installs complete")

print(Settings.Download_prerequesites)
if Settings.Download_prerequesites:
    print("Check imports")
    
    try:
        import yaml
    except:
        os.system('python -m pip install -U "pyyaml"')
    
    try:
        import discord
    except:
        os.system('python -m pip install -U "discord.py[voice]"')

    try:
        import cpuinfo
    except:
        os.system('pip install "py-cpuinfo"')

    try:
        import youtubesearchpython
    except:
        os.system('python3 -m pip install -U "youtube-search-python"')

    try:
        import PIL
    except:
        os.system('python3 -m pip install -U "Pillow"')

    _prev_module = None
    while True:
        try:
            import foaas
            import psutil
            import geopy
            import wavelink
            import pytz
            import bs4
            import requests
            import mcstatus
            import googletrans
            import speedtest
            import art
            import imgurpython
            break
        except ModuleNotFoundError as e:
            x = re.sub("'", "", str(e))
            y = re.sub("No module named ", "", x)
            
            os.system('python3 -m pip install -U "{}"'.format(y))
            if _prev_module == y:
                break
            else:
                _prev_module = y

    print("Installs complete")

if Settings.fix_cert:
    os.system("pip install --upgrade certifi")

# pip install --user --upgrade certifi bs4 requests pyyaml discord.py[voice] wavelink geopy pytz certifi pip


import traceback
import sys

try:
    print("do_stuff()")
except Exception:
    if 'line' in traceback.format_exc():
        print(traceback.format_exc())
