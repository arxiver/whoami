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
    img= img[int(img.shape[0]*0.10):int(img.shape[0]*0.90),int(img.shape[1]*0.04):int(img.shape[0]*0.96)]



    #blur to remove noise
    img =  cv2.medianBlur(img,5)
        
    #black and white 
    binaryImg = ((img > 200)*255).astype('uint8')   
    # cv2.imwrite('binaryImg2.png',binaryImg)

    #remove noise by anding imgblur and binaryImg
    # img[binaryImg==255]=255

    #get contours
    contours,_ = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
      
    Ymin = 0
    Ymax = img.shape[0]
    
    Xmin= img.shape[1]
    Xmax= 0
    newContours=[]
    
    #get two lines
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w < img.shape[1]*0.5 or h >img.shape[0]*0.02 :
                if x <= img.shape[1]*0.5 :  
                    if x>0:
                        Xmin = min(Xmin,int(x))
    
                else:
                    Xmax = max(Xmax,int(x+w))
                newContours.append(contour)
            else:
                if y <= img.shape[0]*0.5:         
                    Ymin = max(Ymin,int(y+h))
                else:
                    Ymax = min(Ymax,int(y))
    
    Ymin2 = Ymax
    Ymax2 = Ymin
    
    #remove white borders
    for contour in newContours:
            x, y, w, h = cv2.boundingRect(contour)
            if y <= (Ymax-Ymin)*0.5: 
                if  y < Ymin2 and y>Ymin:
                    Ymin2 = y
            else:
                if  y+h > Ymax2 and y+h < Ymax:
                    Ymax2 = y+h
    
    #crop both
    if(Ymin2<Ymax2):
        img = img[Ymin2:Ymax2,Xmin:Xmax]
        binaryImg=binaryImg[Ymin2:Ymax2,Xmin:Xmax]
    elif(Ymin<Ymax):
        img = img[Ymin:Ymax,Xmin:Xmax]
        binaryImg=binaryImg[Ymin:Ymax,Xmin:Xmax]

    #return cropped img,cropped binaryImg  
    cv2.imwrite('img.png',img) 
    return img,binaryImg



