from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def calculate_thresh(fname):
    with open(fname) as f:
        content =  [float(x.strip('\n')) for x in f.readlines()]

    a = np.array(content)

    median = np.median(a)
    print(median)
    n = len(a)

    sum = 0
    for i in range(1,n):
        sum = sum + abs(a[i]-a[i-1])

    M = sum/(n - 1)
    print(M)
    lower_thresh = median - 3*M
    upper_thresh = median + 3*M
    
    thresh = []
    thresh.append(lower_thresh)
    thresh.append(upper_thresh)
    return thresh

def plot_time_series(fname,thresh):
    with open(fname) as f:
        content =  [float(x.strip('\n')) for x in f.readlines()]

    a = np.array(content)
    
    x = range(0,len(a))
    y = a
    
    plt.scatter(x,y)
    plt.axhline(y = thresh[0])
    plt.show()

def main():
   
   files = ["voices_time_series.txt","enron_by_day_time_series.txt"]
   for fname in files:
   	thresh = calculate_thresh(fname);
   	plot_time_series(fname, thresh)

if __name__ == '__main__':
	main()
