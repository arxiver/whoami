from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
import numpy as np

def implemented_lbp(img,r):
    mat_center=img[r:-r,r:-r]

    mat0=img[2*r:,r:-r]
    mat0Bool=mat_center>mat0
    mat0Bit=1*mat0Bool

    mat1=img[2*r:,2*r:]
    mat1Bool=mat_center>mat1
    mat1Bit=2*mat1Bool

    mat2=img[r:-r,2*r:]
    mat2Bool=mat_center>mat2
    mat2Bit=4*mat2Bool

    mat3=img[:-2*r,2*r:]
    mat3Bool=mat_center>mat3
    mat3Bit=8*mat3Bool

    mat4=img[:-2*r,r:-r]
    mat4Bool=mat_center>mat4
    mat4Bit=16*mat4Bool

    mat5=img[:-2*r,:-2*r]
    mat5Bool=mat_center>mat5
    mat5Bit=32*mat5Bool

    mat6=img[r:-r,:-2*r]
    mat6Bool=mat_center>mat6
    mat6Bit=64*mat6Bool

    mat7=img[2*r:,:-2*r]
    mat7Bool=mat_center>mat7
    mat7Bit=128*mat7Bool

    LBP=mat0Bit+mat1Bit+mat2Bit+mat3Bit+mat4Bit+mat5Bit+mat6Bit+mat7Bit

    hist = np.histogram(LBP,bins=256)[0]
    return hist


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
    hist = [implemented_lbp(x,r)/(np.shape(x)[0]*np.shape(x)[1]) for x in lines] 
    #shape = 0 
    #for x in lines: 
        #lbp_img = local_binary_pattern(x,points,r) 
        #a,_ = np.histogram(lbp_img,bins=256,range=(0,256)) 
        #a = implemented_lbp(x,r)
        #shape=(np.shape(x)[0]*np.shape(x)[1]) 
        #hist.append(a/shape) 
    return (hist) 

