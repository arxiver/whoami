#!/home/sofyan/anaconda3/bin/python3
import os
import cv2
from preprocessing import preprocessing
from featureExtraction import extractLBP
from featureExtraction import extractLBPLines
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from threading import Thread 
from sklearn import svm
import random

import datetime

class main():

######################################################
#                       INIT                            
######################################################
    def __init__(self):
        self.images = []
        self.imagesPrint = []
        self.tests = []
        self.testsPrint = []
        self.writers = []
        self.yTrain = []
        self.featuresLabled = []
        self.featuresTest = []

        # self.NumOfRuns=n

        self.expected = []
        self.output = []
        self.timers = []

        # pathes
        self.inputPath = "data"
        self.outputPath = "output/results.txt"
        self.timerPath = "output/time.txt"
        self.expectedPath = "output/expected.txt"

        # files 
        self.fOutput = open(self.outputPath, 'w')
        self.fTimer = open(self.timerPath, 'w')

        # self.getExpected()


    def __del__(self):
        self.fOutput.close()
        self.fTimer.close()

######################################################
#                       RE-INIT                            
######################################################
    def reinitialize(self):
        self.images = []
        self.imagesPrint = []
        self.tests = []
        self.testsPrint = []
        self.writers = []
        self.yTrain = []
        self.featuresLabled = []
        self.featuresTest = []

    def sort(self,l):
        for i in range(len(l)):
            for j in range(len(l)):
                if int(l[i]) < int(l[j]):
                    l[i],l[j] = l[j],l[i]

        return l

######################################################
#                READ FILES (TEST BY TEST)                            
######################################################
    def readFiles(self):
        count = 0
        l = self.sort(os.listdir(self.inputPath))
        for test in l:
            # if count == self.NumOfRuns:
            #     break
            # count+=1
            
            for writer in os.listdir(os.path.join(self.inputPath, test)):
                writerImages = []
                writerImagesPrint = []
                if "." in writer:
                    self.tests.append(os.path.join(self.inputPath, test,writer))
                    self.testsPrint.append(os.path.join(self.inputPath, test,writer))
                else:
                    for image in os.listdir(os.path.join(self.inputPath, test,writer)):
                        writerImages.append(os.path.join(self.inputPath, test,writer,image))
                        writerImagesPrint.append(os.path.join(self.inputPath, test,writer,image))
                    self.images.append(writerImages)
                    self.imagesPrint.append(writerImagesPrint)
                    self.writers.append(int(writer))        # the name of the directory must be integer

            self.readImages()
            self.startPipeline()
            self.writeOutput()
            # self.Print()
            self.reinitialize()
            
        # self.calculateAccuracy()


######################################################
#                    READ IMAGES                            
######################################################
    def readImages(self):
        for i in range(len(self.images)):
            for j in range(len(self.images[i])):
                self.images[i][j] = cv2.imread(self.images[i][j], 0)

        for i in range(len(self.tests)):
                self.tests[i] = cv2.imread(self.tests[i], 0)


    def startPipeline(self):

        Start = datetime.datetime.now()


        try:
            thread1 = Thread(target = self.preprocessingAndFeatures, args = (self.images[0][0], self.writers[0],)) 
            thread2 = Thread(target = self.preprocessingAndFeatures, args = (self.images[0][1], self.writers[0],))  
            thread3 = Thread(target = self.preprocessingAndFeatures, args = (self.images[1][0], self.writers[1],))  
            thread4 = Thread(target = self.preprocessingAndFeatures, args = (self.images[1][1], self.writers[1],))  
            thread5 = Thread(target = self.preprocessingAndFeatures, args = (self.images[2][0], self.writers[2],))  
            thread6 = Thread(target = self.preprocessingAndFeatures, args = (self.images[2][1], self.writers[2],))  
            thread7 = Thread(target = self.preprocessingAndFeatures, args = (self.tests[0],None,))

            thread1.start()  
            thread2.start()  
            thread3.start()  
            thread4.start()  
            thread5.start()  
            thread6.start()  
            thread7.start()

            thread1.join()  
            thread2.join()  
            thread3.join()  
            thread4.join()  
            thread5.join()  
            thread6.join()  
            thread7.join()

            output = self.knn()
        except:
            # RANDOM ANSWER IF THERE IS ANY ERROR
            output = [random.randint(1,3)]

        End = datetime.datetime.now()
        self.output.extend(output)
        self.timers.append(str(round((End-Start).total_seconds(),2)))

######################################################
#        START THE PREPROCESSING AND FEATURES                            
######################################################
    def preprocessingAndFeatures(self,img,writer):
        preProcessing, lines = preprocessing(img)
        features = extractLBPLines(lines)

        writerList = [writer]*len(features)
        if writer is not None:
            self.featuresLabled.extend(features)
            self.yTrain.extend(writerList)
        else:
            self.featuresTest.extend(features)

######################################################
#                       KNN                            
######################################################
    def knn(self):
        n=min(len(self.yTrain),7)
        knn = KNeighborsClassifier(n_neighbors=n,weights="distance") 
        knn.fit(self.featuresLabled,self.yTrain) 
        ret = knn.predict(self.featuresTest)
        return [(int(np.argmax(np.bincount(ret))))]
######################################################
#               GET EXPECTED OUTPUT  
######################################################
    def getExpected(self): 
        try:
            with open(self.expectedPath) as file_in:
                for line in file_in:
                    self.expected.append(int(line.rstrip()))
        except:
            print("There is no expected file, there is no accuracy calculated")
######################################################
#               CALCULATE THE ACCURACY                            
######################################################
    def calculateAccuracy(self):

        timerSum = 0
        for x in self.timers:
            timerSum += float(x)


        if(len(self.expected) == 0):
            print("No expected output, no accuracy")
            print("The average time is:",round(timerSum/len(self.timers),2)," sec")
            exit()

        if(len(self.expected) < len(self.output)):
            print("No accuracy cauculated, the number of expected output is less than the number of actual output")
            print("The average time is:",round(timerSum/len(self.timers),2)," sec")
            exit()

        if(len(self.output) == 0):
            print("There are no ouputs, something went wrong, try again")
            exit()

        count = 0
        for i in range(len(self.output)):
            if(self.expected[i] == self.output[i]):
                count+=1
        try:
            accuracy = (count/len(self.output))*100
        except ZeroDivisionError:
            print("Can't calculate the accuracy, the output list is empty")

        print("The accuracy is:",round(accuracy,2),"%")
        print("The average time is:",round(timerSum/len(self.timers),2)," sec")

######################################################
#                WRITE THE OUTPUT  
######################################################
    def writeOutput(self):        
        self.fOutput.write(str(self.output[len(self.output)-1])+'\n') 
        self.fTimer.write(str(self.timers[len(self.timers)-1])+'\n') 

######################################################
#                       PRINT         
######################################################

    # Assumtion: The len of tests and output is 1
    
    def Print(self):
        if(len(self.tests) == 0 or len(self.output) == 0):
            raise Exception("The lenght of tests or output is zero, wrong")
        
        print("Processing the image ->",self.testsPrint[0])
        if(len(self.expected) >= len(self.output)):
            print("The expected output is: ",self.expected[len(self.output)-1])
        else:
            print("The expected output is: ",None)
        
        print("The actual output is: ",self.output[len(self.output)-1])

        if(len(self.expected) >= len(self.output)):
            if(self.expected[len(self.output)-1] != self.output[len(self.output)-1]):
                print("Error")
        print("=========================================================")

######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    obj = main()
    obj.readFiles()
