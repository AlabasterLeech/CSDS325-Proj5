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
import scipy

SINGLE_SITE = 'adobe.com'
SHOW_FIGS = True
MAKE_FIGS = [False, False, True]

WEEKDAY_DICT = { #0 = Monday, 6 = Sunday
    "11-28":1,
    "11-29":2,
    "11-30":3,
    "12-01":4,
    "12-02":5,
    "12-03":6,
    "12-04":0,
    "12-05":1,
    "12-06":2,
    "12-07":3
    }

dataMaster = []
with open('main-data.csv',newline = '') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for line in datareader:
        if(line[2] != 'domaincontrol.com'):
            dataMaster.append(tuple([line[0],line[1],line[2],int(line[3])]))




if(MAKE_FIGS[0]):
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
    timeofDayR = scipy.stats.pearsonr(hourAvgs, range(24))
    print(timeofDayR)

if(MAKE_FIGS[1]):
    hourTotals = [0]*24
    hourCounts = [0]*24
    hourAvgs = [0]*24

    for entry in (y for y in dataMaster if y[2] == SINGLE_SITE):
        hourTotals[int(entry[0][11:13])] += entry[3]
        hourCounts[int(entry[0][11:13])] += 1

    for x in range(24):
        hourAvgs[x] = hourTotals[x]/hourCounts[x]

    print(hourCounts)
    print(hourTotals)

    figTODPlot, axTODPlot = plt.subplots()
    axTODPlot.scatter(range(24), hourAvgs)
    axTODPlot.set_xlim([0,23])
    axTODPlot.set_ylim([0,15])
    axTODPlot.set_title("Average tracert Hops vs. Hour Of Day for " + SINGLE_SITE)
    axTODPlot.set_xlabel("Hour of Day")
    axTODPlot.set_ylabel("Average number of hops")
    timeofDayR = scipy.stats.pearsonr(hourAvgs, range(24))
    print(timeofDayR)

if(MAKE_FIGS[2]):
    weekdayTotals = [0]*7
    weekdayCounts = [0]*7
    weekdayAvgs = [0]*7

    for entry in dataMaster:
        weekdayTotals[WEEKDAY_DICT[entry[0][5:10]]] += entry[3]
        weekdayCounts[WEEKDAY_DICT[entry[0][5:10]]] += 1
    for x in range(7):
        weekdayAvgs[x] = weekdayTotals[x]/weekdayCounts[x]

    figDOWPlot, axDOWPlot = plt.subplots()
    axDOWPlot.scatter(range(7), weekdayAvgs)
    axDOWPlot.set_xlim([-0.1,6.1])
    axDOWPlot.set_ylim([14.6,14.9])
    axDOWPlot.set_title("Average tracert Hops vs. Day of the Week")
    axDOWPlot.set_xlabel("Day of Week")
    axDOWPlot.set_ylabel("Average number of hops")
    axDOWPlot.set_xticks([0,1,2,3,4,5,6],["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", "Sunday"], rotation=20)
    dowR = scipy.stats.pearsonr(weekdayAvgs, range(7))
    print(dowR)

if(SHOW_FIGS):
    plt.show()
