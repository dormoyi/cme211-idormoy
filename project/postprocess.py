### NOTE: this file wasn't tested on rice!


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys



if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage:")
        print(" $ python3 postprocess.py input1.txt solution<#>")
        sys.exit(0)
        
    # assign arguments
    input, solution = sys.argv[1], sys.argv[2]
    print("Input file processed: " + input)
    
    # initialize the temperatures array with the boundaries conditions
    f1 = open(input, 'r')
    matrix = f1.readlines()
    f1.close()
    length , width , height = matrix[0].split(' ')
    Tc, Th = matrix[1].split(' ')
    Tc, Th = float(Tc), float(Th)
    length , width , height = float(length) , float(width) , float(height)
    nrows, ncols = int(width/height), int(length/height)
    X = np.linspace(0, length, int(length/height))
    Y = np.linspace(0, width, int(width/height))

    # boundary conditions
    arr = np.zeros((nrows, ncols))
    for j in range(ncols):
        arr[0][j] = Th # upper bound condition
        arr[nrows-1][j] = -Tc*np.exp(-10*(j*height-length/2)**2-2)

    # get the rest of the temperatures from the C++ solver
    f1 = open(solution, 'r')
    sols = f1.readlines()
    f1.close()
    k = 0
    for j in range(ncols):
        for i in range(1, nrows-1):
            arr[i][j] = float(sols[k])
            k+=1

    # plot the result
    print("Mean Temperature: " + str(round(np.mean(arr),4)))
    plt.figure()    
    plt.pcolormesh(X,-Y, arr)
    plt.colorbar()
    plt.xlim(-0.05*length, length*1.05)
    plt.ylim(-1.8*width, 0.8*width)
    X, Y = np.meshgrid(X,Y)
    plt.contour(X,-Y, arr, levels=[np.mean(arr)]) # isoline
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig('plot.png')
    plt.show()


