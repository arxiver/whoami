from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
import numpy as np

def extractLBP(img):
    #takes an image and returns an array of 256 values that represent the histogram values
    grey = img   #ignore if it is already grey
    r = 5 #change this for different details
    points = 8 #changing this will result in a different size for the histogram array
    lbp_img = local_binary_pattern(grey,points,r)
    a,_ = np.histogram(lbp_img,bins=256,range=(0,256))
    return a

    # 1
    # 5 => 90 %
    # 3 => 85 %
    # 1 => 95 %

    # 2
    # 5 => 85 %
    # 3 => 85 %
    # 1 => 75 %

    # 3
    # 5 => 85 %
    # 3 => 80 %
    # 1 => 85 %


def extractLBPLines(lines): 
    r = 3 
    points = 8 
    hist = [] 
    shape = 0 
    for x in lines: 
        lbp_img = local_binary_pattern(x,points,r) 
        a,_ = np.histogram(lbp_img,bins=256,range=(0,256)) 
        shape=(np.shape(x)[0]*np.shape(x)[1]) 
        hist.append(a/shape) 
    return (hist) 