import os
import importlib.util
import zipfile
import sys
import zipfile
import tarfile
import platform
import code
import subprocess
import datetime
import socket
import atexit
import shlex
import builtins
import hashlib
try:
    import curses
    import psutil
    import speedtest
    import requests
    system = platform.system()
    if system in ("Darwin", "Linux"):
        import curses
        import readline 
    elif system in ("Windows"):
        try:
            import curses
        except ImportError:
            import windows_curses as curses
        import pyreadline3
except ModuleNotFoundError:
    print("your system doesn't has some python Module to run , do you want install?")
    while True:
        install = input("(y/n):")
        if install.lower() == "y":
            try:
                system = platform.system() 
                subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "speedtest-cli"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
                if system in ("Darwin", "Linux"):
                    subprocess.run([sys.executable, "-m", "pip", "install", "curses"], check=True)
                    subprocess.run([sys.executable, "-m", "pip", "install", "readline"], check=True)
                    import readline
                    import psutil
                    import requests
                    import speedtest
                    import curses
                    break
                elif system in ("Windows"):
                    subprocess.run([sys.executable, "-m", "pip", "install", "windows-curses"], check=True)
                    subprocess.run([sys.executable, "-m", "pip", "install", "pyreadline3"], check=True)
                    import pyreadline3
                    import psutil
                    import requests
                    import speedtest
                    try:
                        import curses
                        break
                    except ImportError:
                        import windows_curses as curses
                        break
            except Exception as e:
                print("Error:", e)
                #print("does pip installed on your python? if error not installed choose y")
                #while True:
                    #install_pip_question = input("(y/n):")
                    #if install_pip_question.lower() == "y":
                        #try:
                            #subprocess.run([sys.executable, "get-pip.py"], check=True)
                        #except Exception as e:
                            #print("Error installing pip:", e)
                    #if install_pip_question.lower() == "n":
                        #run = False
                        #break
                    #else:
                        #print("error, only use y/n")

                run = False
                break
        if install.lower() == "n":
            run = False
            break
        else:
            print("error, only use y/n")
    
import time
import shutil
def test():
    print("Hello world")\
                 

