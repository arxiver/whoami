# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:55:47 2021

@author: Khaled
"""

import cv2
import numpy as np



#takes image and return cropped image without noise and cropped binary image without noise
def preprocessing(img):

    #crop noise on borders
	img= img[int(img.shape[0]*0.04):int(img.shape[0]*0.96),int(img.shape[1]*0.04):int(img.shape[0]*0.96)]
    
	#blur to remove noise
    img =  cv2.medianBlur(img,5)
        
    #black and white 
    binaryImg = ((img > 200)*255).astype('uint8')   
    cv2.imwrite('binaryImg2.png',binaryImg)
    
    #remove noise by anding imgblur and binaryImg
    img[binaryImg==255]=255
    
    #get contours
    im2,contours, hierarchy = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    Ymin = 0
	Ymax = img.shape[0]

    for contour in contours:
			x, y, w, h = cv2.boundingRect(contour)
			if w < img.shape[1]*0.5 or h >img.shape[0]*0.02 :
				continue

			if y <= img.shape[0]*0.5:         
				Ymin = max(Ymin,int(y+h))
			else:
				Ymax = min(Ymax,int(y-h))
    
    
	#crop both
	if(Ymin<Ymax):
		img = img[Ymin:Ymax,:]
		binaryImg=binaryImg[Ymin:Ymax,:]

    
    #remove white borders
    cord=np.where(binaryImg==0)
    img = img[min(cord[0]):max(cord[0]),min(cord[1]):max(cord[1])]
    binaryImg = binaryImg[min(cord[0]):max(cord[0]),min(cord[1]):max(cord[1])]
    
    #return cropped img,cropped binaryImg  
    return img,binaryImg
    
    

