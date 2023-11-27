from subprocess import Popen, PIPE
import sys

IPINFO_TOKEN = 93e8f08e16f680

def tracer(host=None):
    p = Popen(['tracert', host], stdout=PIPE)
    while True:
        try:
            line = p.stdout.readline()
            if not line:
                break
            print (line.rstrip())
        except:
            break

tracer('8.8.8.8')
