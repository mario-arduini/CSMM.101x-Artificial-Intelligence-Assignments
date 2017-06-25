import pandas as pd
import numpy as np
import sys

# plot points and plane
def plotall(dset):
    import matplotlib.pyplot as plt
    plt.plot(dset[0][yi==1],dset[1][yi==1],"or")
    plt.plot(dset[0][yi==-1],dset[1][yi==-1],"ob")
    plt.show()

def main():
    # read data from input, expected csv, 2 feature and 1 label
    fin = sys.argv[1]
    dset = pd.read_csv(fin)

    # prepare output
    fout = sys.argv[2]
    f = open(fout,"w")


    f.close()

    # plot if required
    if len(sys.argv)>3 and sys.argv[3] == '-plot':
        plotall(dset,beta)

if __name__ == "__main__" :
    main()
