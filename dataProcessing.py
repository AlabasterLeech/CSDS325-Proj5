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
MAKE_FIGS = [False, False, False, True, True]

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

DOMAIN_DICT = {
    "google.com":0,
    "amazonaws.com":1,
    "facebook.com":2,
    "microsoft.com":3,
    "apple.com":4,
    "youtube.com":5,
    "twitter.com":6,
    "azure.com":7,
    "cloudflare.com":8,
    "gstatic.com":9,
    "digicert.com":10,
    "linkedin.com":11,
    "doubleclick.net":12,
    "live.com":13,
    "wikipedia.org":14,
    "fastly.net":15,
    "bing.com":16,
    "wordpress.org":17,
    "yahoo.com":18,
    "pinterest.com":19,
    "github.com":20,
    "ui.com":21,
    "tiktokv.com":22,
    "spotify.com":23,
    "adobe.com":24,
    "vimeo.com":25,
    "gandi.net":26,
    "sharepoint.com":27,
    "zoom.us":28,
    "wordpress.com":29,
    "bit.ly":30,
    "qq.com":31,
    "msn.com":32,
    "app-measurement.com":33,
    "yandex.ru":34,
    "blogspot.com":35,
    "whatsapp.net":36,
    "cloudflare.net":37,
    "skype.com":38,
    "nic.ru":39,
    "reddit.com":40,
    "roblox.com":41,
    "opera.com":42,
    "snapchat.com":43,
    "criteo.com":44,
    "dropbox.com":45,
    "baidu.com":46,
    "intuit.com":47,
    "icir.org":48,
    }

dataMaster = []
x = 0
with open('main-data.csv',newline = '') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for line in datareader:
        if(line[2] != 'domaincontrol.com'):
            if(line[1][14:16] == '00' and int(line[0][14:16]) > 50):
                duration = float(line[1][17:]) + 60*(60+float(line[1][14:16])) - (float(line[0][17:]) + 60*float(line[0][14:16]))
            else:
                duration = float(line[1][17:]) + 60*+float(line[1][14:16]) - (float(line[0][17:]) + 60*float(line[0][14:16]))
            dataMaster.append(tuple([line[0],line[1],line[2],int(line[3]),duration]))

dataDist = []
with open('nslookup-results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for line in reader:
        dataDist.append(tuple([line[0], line[1], line[2]]))

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

if(MAKE_FIGS[3]):
    domainTotals = [0]*49
    domainCounts = [0]*49
    domainAvgs = [0]*49
    domainAvgsGoodDist = []

    for entry in dataMaster:
        domainTotals[DOMAIN_DICT[entry[2]]] += entry[3]
        domainCounts[DOMAIN_DICT[entry[2]]] += 1
    for x in range(49):
        domainAvgs[x] = domainTotals[x]/domainCounts[x]

        print(dataMaster[x][2] + "," + str(domainAvgs[x]))
        
        if(dataDist[x][2] != 'NC'):
            domainAvgsGoodDist.append(domainAvgs[x])

    

    figDistPlot, axDistPlot = plt.subplots()
    axDistPlot.scatter([int(x[2]) for x in dataDist if x[2] != 'NC'], domainAvgsGoodDist)
    axDistPlot.set_title("Average tracert Hops vs. Physical Distance")
    axDistPlot.set_xlabel("Physical Distance From Desktop (miles)")
    axDistPlot.set_ylabel("Average number of hops")
    distR = scipy.stats.pearsonr([int(x[2]) for x in dataDist if x[2] != 'NC'], domainAvgsGoodDist)
    print(distR)

if(MAKE_FIGS[4]):
    figTimePlot, axTimePlot = plt.subplots()
    axTimePlot.scatter([x[3] for x in dataMaster], [x[4] for x in dataMaster], s = 1)
    axTimePlot.set_title("Duration of tracert vs. Number of Hops in Route")
    axTimePlot.set_xlabel("Number of Hops")
    axTimePlot.set_ylabel("Time Elapsed")
    timeR = scipy.stats.pearsonr([x[3] for x in dataMaster], [x[4] for x in dataMaster])
    print(timeR)

if(SHOW_FIGS):
    plt.show()
