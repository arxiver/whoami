from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
import numpy as np

def extractLBP(img):
    #takes an image and returns an array of 256 values that represent the histogram values
    grey =rgb2gray(img)  #ignore if it is already grey
    r = 1 #change this for different details
    points = 8 #changing this will result in a different size for the histogram array
    lbp_img = local_binary_pattern(grey,points,r)
    a,_ = np.histogram(lbp_img,bins=256,range=(0,256))
    return a

