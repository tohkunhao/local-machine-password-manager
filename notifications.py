__author__ = "github.com/tohkunhao"
__version__ = "0.1"

from time import sleep
import os

def error_msg(msg, do_clear=False):
    print(msg)
    sleep(1.5)
    if do_clear:
        clear_screen()

def clear_screen():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")

def countdown_timer(msg, seconds):
    for i in range(seconds,0,-1):
        print(msg+" "+f"{i}  ", end = "\r")
        sleep(1)
