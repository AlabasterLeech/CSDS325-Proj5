from subprocess import Popen, PIPE
import subprocess as sp
import sys
from ischedule import schedule, run_loop
import time
from datetime import datetime


INPUT_FILE_NAME = 'cand3.txt'

candidates = []


def runNSL(host=None):
    p = Popen(['tracert', '-h', '1', host], stdout=PIPE, creationflags=sp.CREATE_NO_WINDOW)

    while True:
        try:
            line = p.stdout.readline()
            if not line:
                break
            print(line)
        except:
            break


with open(INPUT_FILE_NAME) as file:
    candidates = [line.rstrip() for line in file]

for candidate in candidates:
    runNSL(candidate)
