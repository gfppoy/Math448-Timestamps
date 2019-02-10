# -*- coding: utf-8 -*-
"""
Timestamp Test Set Generator

Generates sets of CSV files containing timestamps with specified degrees of:
    - regularity (based on StDev of timestamp differences)
    - acceleration (change in timestamp differences)
    - clustering (proportion of timestamps close to some underlying pattern)

for MATH 448
by Jamie Dunkle, UBC 2019
"""


import time
import csv
from datetime import datetime,timedelta
import numpy as np


def regSeqDates(start, format, mean, std, acc, n):
    """Generate a sequence of timestamps with a given interval mean and stdev.
    
    start and end should be strings specifying times formated in the
    given format (strftime-style).
    mean and stdev should be a float representing interval in hours. 1.0 = 1 hr
    acc is the ratio of acceleration
    The returned list of times will be in the specified format. 
    """
    
    stime = time.mktime(time.strptime(start, format))
    prev_ts = datetime.fromtimestamp(stime)
    start_ts = time.localtime(time.mktime(prev_ts.timetuple()))
    ts = [time.strftime(format, start_ts)]
    
    while True:
        norm_sample = np.random.normal(mean, std, n-1)
        
        intervals = np.ones_like(norm_sample) * mean
    
        deviations = norm_sample - intervals
        mid_idx = (n-1) / 2
    
        for r in range(0, n-1):
            intervals[r] = intervals[r]*np.power(acc, r-mid_idx)
        
        intervals = intervals + deviations
    
        if acc != 1.0 and all(intervals > 1.0):
            break
    
        if np.abs(np.std(intervals) - std) < 0.01 and all(intervals > 1.0):
            break
        
    print intervals, np.mean(intervals), np.std(intervals)
    
    for i in intervals:
        next_time = prev_ts + timedelta(minutes=i)
        prev_ts = next_time
        dtime = time.localtime(time.mktime(next_time.timetuple()))
        ts.append(time.strftime(format, dtime))
    return ts


start_ts = "1/1/2019 12:00 AM"
ts_format  = '%m/%d/%Y %I:%M %p'

stdevs = [0.0, 5.0, 10.0, 15.0, 20.0]
accels = [0.8, 0.9, 1.0, 1.1, 1.2]
n = 20
mean = 60.0

for std in stdevs:
    for acc in accels:
        dateSeq = regSeqDates(start_ts, ts_format, mean, std, acc, n)

        # Write text file
        output_fname = ('timestamps_n' +str(n)+ '_' + str(int(mean)) + 'mins_' + 
                        'std' + str(int(std)) +
                        '_acc' + str(int(acc*100)) + '.txt')
        
        myFile = open(output_fname, 'w')
        with myFile:
            writer = csv.writer(myFile, dialect='excel')
            for ds in dateSeq:
                writer.writerow([ds])
        
        
# READ TXT FILE
#with open('dateseq.txt') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#    for row in csv_reader:
#        print row