# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:55:47 2021

@author: Khaled
"""

import cv2
import numpy as np



#takes image and return cropped image without noise and lines
def preprocessing(img):

    #crop noise on borders
    img= img[int(img.shape[0]*0.12):int(img.shape[0]*0.75),int(img.shape[1]*0.04):int(img.shape[0]*0.96)]
    
    
    
    #blur to remove noise
    img =  cv2.medianBlur(img,5)
        
    #black and white 
    binaryImg = ((img > 200)*255).astype('uint8')   
    
    
    
    #remove noise by anding img and binaryImg
    img[binaryImg==255]=255
    
    #get contours
    contours,_ = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    Ymin = 0
    Ymax = img.shape[0]
    
    Xmin= img.shape[1]
    Xmax= 0
    #get two lines to get handwriting only and get Xmin ,Xmax remove white borders on sides
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if x==0:
                continue
            if w < img.shape[1]*0.5 or h >img.shape[0]*0.02 :
                if x <= img.shape[1]*0.5:  
                        Xmin = min(Xmin,int(x))
    
                else:
                    Xmax = max(Xmax,int(x+w))
    
            else:
                if y <= img.shape[0]*0.5:         
                    Ymin = max(Ymin,int(y+h))
                else:
                    Ymax = min(Ymax,int(y))
    
    Ymin2 = Ymax
    Ymax2 = Ymin
    
    
    #get Ymin and Ymax to remove white borders top and bottom
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if y <= (Ymax-Ymin)*0.5: 
                if  y < Ymin2 and y>Ymin:
                    Ymin2 = y
            else:
                if  y+h > Ymax2 and y+h < Ymax:
                    Ymax2 = y+h
    
    #crop img and binaryImg
    if(Ymin2<Ymax2):
        img = img[Ymin2:Ymax2,Xmin:Xmax]
        binaryImg=binaryImg[Ymin2:Ymax2,Xmin:Xmax]
    elif(Ymin<Ymax):
        img = img[Ymin:Ymax,Xmin:Xmax]
        binaryImg=binaryImg[Ymin:Ymax,Xmin:Xmax]
    
    binaryImgCopy=np.copy(binaryImg)
    #erode to make lines -> black boxes
    kernel = np.ones((1,int(binaryImg.shape[1]*0.08)),np.uint8)
    binaryImg =cv2.erode(binaryImg,kernel,iterations = 1)
    
    #crop borders to get right Contours
    binaryImg[:,0:10]=255
    binaryImg[0:10,:]=255
    binaryImg[:,binaryImg.shape[1]-10:]=255
    binaryImg[binaryImg.shape[0]-10:,:]=255
    
    contours,_ = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #image for every line
    lines=[]
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if x==0 or h < img.shape[0]*0.01  or  w < img.shape[1]*0.2 :
                continue
            lines.append(img[y:y+h,x:x+w])
            lines.append(binaryImgCopy[y:y+h,x:x+w])

    #return cropped img,lines 
    return img,lines



