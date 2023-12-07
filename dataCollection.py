from subprocess import Popen, PIPE
import subprocess as sp
import sys
from ischedule import schedule, run_loop
import time
from datetime import datetime

WINDOWS_TRACERT_HOP_SPACING = 4
INPUT_FILE_NAME = 'cand3.txt'
OUTPUT_FILE_NAME = 'output.txt'

candidates = []
numDataPoints = 0

def runTraceCountHops(host=None):
    p = Popen(['tracert', '-w', '200', host], stdout=PIPE, creationflags=sp.CREATE_NO_WINDOW)
    hops = 0
    while True:
        try:
            line = p.stdout.readline()
            if not line:
                break
            if(line[0:WINDOWS_TRACERT_HOP_SPACING].strip().isdigit() and int(line[0:4].strip()) == hops + 1):
                hops += 1
        except:
            break

    return hops


def createDataPoint():
    global numDataPoints
    host = candidates[numDataPoints%len(candidates)]
    dataFile = open(OUTPUT_FILE_NAME, "a")
    start = str(datetime.now())
    hops = runTraceCountHops(host)
    end = str(datetime.now())
    dataFile.write(start + "," + end + "," + host + "," + str(hops) + "\n")
    dataFile.close()
    numDataPoints += 1
    if(numDataPoints % 25 == 1):
        print("Collected " + str(numDataPoints) + " data points. Program running")


with open(INPUT_FILE_NAME) as file:
    candidates = [line.rstrip() for line in file]

schedule(createDataPoint, interval=60)
run_loop()
