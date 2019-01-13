import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

def main(argv):
    parser = ArgumentParser()
    parser.add_argument("-c", "--channel", dest="channel", help="channel id")

    args = parser.parse_args()

    data = np.load('output/%s.npy' % args.channel)

    for i in range(len(data)):
        arr = data[i]
        ax1 = plt.subplot(5, 2, i + 1)
        ax1.plot(np.arange(len(arr)), (~np.array(arr).astype(bool)).astype(int))

    plt.savefig('output/%s.png' % args.channel)

if __name__ == "__main__":
   main(sys.argv[1:])
