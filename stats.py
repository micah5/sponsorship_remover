import sys
import numpy as np
import datetime
import math
from argparse import ArgumentParser

def pretty_date(seconds):
    return str(datetime.timedelta(seconds=math.ceil(seconds)))

def main(argv):
    parser = ArgumentParser()
    parser.add_argument("-c", "--channel", dest="channel", help="channel id")

    args = parser.parse_args()

    data = np.load('output/%s.npy' % args.channel)

    sum_avg = 0
    for list in data:
        arr = np.array(list)
        sum_avg += np.count_nonzero(arr==0)/arr.size

    avg = sum_avg/data.size
    print('Avg of video that is sponsorship:', round(avg*100), '%')
    print('Avg time of sponsorship:', pretty_date(np.count_nonzero(arr==0)*5), '%')

if __name__ == "__main__":
   main(sys.argv[1:])
