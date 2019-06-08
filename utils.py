from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from PIL import Image
import array
import sys
import os



# Reading Header file
def hdr_read(path):
    row = 0
    col = 0
    bands = 0
    datatype = None
    with open(path, "r") as f:
        for l in f:
            k = l.split()
            if k[0] == "BANDS:":
                bands = k[1]
            elif k[0] == 'ROWS:':
                row = k[1]
            elif k[0] == 'COLS:':
                col = k[1]
            elif k[0] == 'DATATYPE:':
                datatype = k[1]
    mul, D_type = (255, 'uint8') if datatype == 'U8' else ((2**16-1), 'U16')
    print(mul, D_type)
    row = int(row)
    col = int(col)
    bands = int(bands)
    return row, col, bands, datatype



# Reading Image file
def ReadBilFile(bil,bands,pixels):
    extract_band = 1
    image = np.zeros([pixels, bands], dtype=np.uint16)
    gdal.GetDriverByName('EHdr').Register()
    img = gdal.Open(bil)
    while bands >= extract_band:
        bandx = img.GetRasterBand(extract_band)
        datax = bandx.ReadAsArray()
        temp = datax
        store = temp.reshape(pixels)
        for i in range(pixels):
            image[i][extract_band - 1] = store[i]
        extract_band = extract_band + 1
    return image



# Returns a numpy array after thresholding
def thresholding(Y, threshold):
    for i in range (Y.shape[0]):
        if(Y[i, :] < threshold):
            Y[i, :] = 0
        else:
            Y[i, :] = Y[i, :]
    return Y



# Returns a numoy array after linear thretching its pixels
def linear_stretch(y_test):
    minima = np.amin(y_test)
    maxima = np.amax(y_test)
    den = maxima-minima
    Y = ((y_test-minima)/ den)*(2**8 - 1)
    return(Y)



# Takes matrix, no. of rows/col, and name with which image is to be saved
# Returns a display on screen and saves the image with the given name
def display_save_image(y, row, col, name):
    img = y.reshape(row, col)
    plt.imshow(img)
    plt.show()
    plt.savefig(name + '.png')
    
    
    
# SOFT CLASSIFIER
def extract_membership(y, class_no):
    Y = y[:, class_no].reshape(y.shape[0], 1)
    return(Y)

