import pandas as pd
import numpy as np
import sys

def main():
    # read data from input, expected csv, 2 feature and 1 label
    fin = sys.argv[1]
    dset = pd.read_csv(fin,header=None)
    data = np.array([np.ones(len(dset)),dset[0],dset[1]]).T
    yi = np.array(dset[2])

    # prepare output
    fout = sys.argv[2]
    f = open(fout,"w")

    # initialize weights
    w = np.ones(3)
    wold = np.array([-1,-1,-1])

    # perceptron algorithm
    while not (w==wold).all() :
        wold = w.copy()
        for i,xi in enumerate(data):
            if np.sum(xi*w)*yi[i] < 0 :
                w += xi*yi[i]
                f.write(str(w[1])+','+str(w[2])+','+str(w[0])+'\n')

    # save results
    f.write(str(w[1])+','+str(w[2])+','+str(w[0])+'\n')
    f.close()

    # plot if required
    if len(sys.argv)>3 and sys.argv[3] == '-plot':
        import matplotlib.pyplot as plt
        plt.plot(dset[0][yi==1],dset[1][yi==1],"or")
        plt.plot(dset[0][yi==-1],dset[1][yi==-1],"ob")
        xval = np.arange(15)
        plt.plot(xval,-w[1]*xval/w[2]-w[0]/w[2])
        plt.show()


if __name__ == "__main__" :
    main()
