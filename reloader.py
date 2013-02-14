from shutil import move
from sys import exit
import os.path
from subprocess import Popen

if os.path.isfile('TrafficAligner_update.py'):
    move("TrafficAligner", "TrafficAligner")


Popen("./TrafficAligner", shell=True)

exit("exit to restart the true program")