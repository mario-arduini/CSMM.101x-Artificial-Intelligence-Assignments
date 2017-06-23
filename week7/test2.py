import pandas as pd
import numpy as np
import sys

def main():
    # read data from input, expected csv, 2 feature and 1 label
    fin = sys.argv[1]
    dset = pd.read_csv(fin,header=None)

    # create feature matrix and label vector
    data = np.array([np.ones(len(dset)),(dset[0]-np.mean(dset[0]))/np.std(dset[0]),(dset[1]-np.mean(dset[1]))/np.std(dset[1])]).T
    yi = np.array(dset[2])

    # learning rates, iteration's number
    alfa = .1
    its = 100

    # Gradient descend
    beta = np.zeros(3)
    for i in range(its):
        beta[0] = beta[0] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,0])/len(data)
        beta[1] = beta[1] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,1])/len(data)
        beta[2] = beta[2] - alfa*np.sum((np.sum(beta*data,axis=1)-yi)*data[:,2])/len(data)
        print(beta)


    # plot if required
    if True or len(sys.argv)>3 and sys.argv[3] == '-plot':
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #ax.scatter(dset[0],dset[1],dset[2],"or")
        xr = np.linspace(1,10,20)
        yr = np.linspace(1,70,20)
        ax.scatter(xr,yr,beta[0]+beta[1]*xr+beta[2]*yr,color="b")
        ax.set_xlabel('Age')
        ax.set_ylabel('Weight')
        ax.set_zlabel('Height')
        plt.show()


if __name__ == "__main__" :
    main()
