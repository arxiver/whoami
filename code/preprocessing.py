# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:55:47 2021

@author: Khaled
"""

import cv2
import numpy as np



#takes image and return cropped image without noise and cropped binary image without noise
def preprocessing(img):
    #img = cv2.imread("3.png",0)
    
    #blur to remove noise
    img =  cv2.medianBlur(img,5)
        
    #black and white 
    binaryImg = ((img > 200)*255).astype('uint8')   
    cv2.imwrite('binaryImg2.png',binaryImg)
    
    #remove noise by anding imgblur and binaryImg
    img[binaryImg==255]=255
    
    #get contours
    im2,contours, hierarchy = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    Ymin = img.shape[1]
    Ymax = 0
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w < img.shape[1]*0.8 or y<img.shape[1]*0.2:
                continue
            Ymin = min(Ymin,(y+h))
            Ymax = max(Ymax,(y-h))
    
    
    #crop both
    img = img[Ymin:Ymax,:]
    binaryImg=binaryImg[Ymin:Ymax,:]
    
    #remove white borders
    cord=np.where(binaryImg==0)
    img = img[min(cord[0]):max(cord[0]),min(cord[1]):max(cord[1])]
    binaryImg = binaryImg[min(cord[0]):max(cord[0]),min(cord[1]):max(cord[1])]
    
      
    return img,binaryImg
    
    
    #cv2.imwrite('binaryImg.png',binaryImg)
    
    
    #cv2.imwrite('img.png',img)
