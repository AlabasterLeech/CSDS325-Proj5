from subprocess import Popen, PIPE
import sys
import csv

def tracer(host=None):
    p = Popen(['tracert', '-w', '500', host], stdout=PIPE)
    lineCount = 0
    while True:
        try:
            line = p.stdout.readline()
            if not line:
                break
            print (line.rstrip())
            lineCount += 1
        except:
            break

tracer('8.8.8.8')
