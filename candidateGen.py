from subprocess import Popen, PIPE
import subprocess as sp
import sys
import csv

SITES_TO_TEST = 1000
MIN_LINES_GOOD_TRACE = 4
MAX_LINES_GOOD_TRACE = 30

def tracer(host=None):
    p = Popen(['tracert', '-w', '250', host], stdout=PIPE, creationflags=sp.CREATE_NO_WINDOW)
    lineCount = 0
    while True:
        try:
            line = p.stdout.readline()
            if not line:
                break
            lineCount += 1
        except:
            break

    return lineCount

with open('tranco-20231113.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    next(csvreader)
    sitesTested = 0
    candidatesAccepted = []
    
    for line in csvreader:
        if(sitesTested >= SITES_TO_TEST = 1000):
            break
        traceResult = tracer(line[1])
        if traceResult > MIN_LINES_GOOD_TRACE and MAX_LINES_GOOD_TRACE < 30:
            candidatesAccepted.append(line[1])
            print('Candidate accepted')
        else:
            print('Candidate rejected')
        sitesTested += 1

    for candidate in candidatesAccepted:
        print(candidate)

    
