import pandas as pd
import numpy as np
import sys

def main():
    # read data from input, expected csv, 2 feature and 1 label
    fin = sys.argv[1]
    dset = pd.read_csv(fin,header=None)

    # standardize data
    dset[0] = (dset[0]-np.mean(dset[0]))/np.std(dset[0])
    dset[1] = (dset[1]-np.mean(dset[1]))/np.std(dset[1])

    # create feature matrix and label vector
    data = np.array([np.ones(len(dset)),dset[0],dset[1]]).T
    yi = np.array(dset[2])

    # prepare output
    fout = sys.argv[2]
    f = open(fout,"w")

    # learning rates, iteration's number
    alfas = np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10])
    its = 100

    # Gradient descend
    for alfa in alfas:
        beta = np.zeros(3)
        for i in range(its):
            beta[0] = beta[0] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,0])/len(data)
            beta[1] = beta[1] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,1])/len(data)
            beta[2] = beta[2] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,2])/len(data)
        # save results
        f.write(str(alfa)+","+str(its)+","+str(beta[0])+","+str(beta[1])+","+str(beta[2])+"\n")
    f.close()

    # plot if required
    if len(sys.argv)>3 and sys.argv[3] == '-plot':
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(dset[0],dset[1],dset[2],"or")
        xr = np.arange(-3,4)
        yr = np.arange(-3,4)
        ax.plot_surface(xr,yr,beta[0]+beta[1]*xr+beta[2]*yr)
        ax.set_xlabel('Age')
        ax.set_ylabel('Weight')
        ax.set_zlabel('Height')
        plt.show()


if __name__ == "__main__" :
    main()
