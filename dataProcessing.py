from subprocess import Popen, PIPE
import subprocess as sp
import sys
from ischedule import schedule, run_loop
import time
from datetime import datetime
import random
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d

SINGLE_SITE = 'azure.com'

dataMaster = []
with open('main-data.csv',newline = '') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for line in datareader:
        if(line[2] != 'domaincontrol.com'):
            dataMaster.append(tuple([line[0],line[1],line[2],int(line[3])]))

hourTotals = [0]*24
hourCounts = [0]*24
hourAvgs = [0]*24

for entry in dataMaster:
    hourTotals[int(entry[0][11:13])] += entry[3]
    hourCounts[int(entry[0][11:13])] += 1

for x in range(24):
    hourAvgs[x] = hourTotals[x]/hourCounts[x]

figTODPlot, axTODPlot = plt.subplots()
axTODPlot.scatter(range(24), hourAvgs)
axTODPlot.set_xlim([0,23])
axTODPlot.set_ylim([14,15.5])
axTODPlot.set_title("Average tracert Hops vs. Hour Of Day")
axTODPlot.set_xlabel("Hour of Day")
axTODPlot.set_ylabel("Average number of hops")


plt.show()
