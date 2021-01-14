#!/home/sofyan/anaconda3/bin/python3
import os
import cv2
from preprocessing import preprocessing
from featureExtraction import extractLBP
from sklearn.neighbors import KNeighborsClassifier

import datetime

class i_o():

######################################################
#                       INIT                            
######################################################
    def __init__(self, n):
        self.images = []
        self.imagesPrint = []
        self.tests = []
        self.testsPrint = []
        self.writers = []
        self.featuresLabled = []
        self.featuresTest = []

        self.NumOfRuns=n

        self.expected = []
        self.output = []
        self.timers = []

        # pathes
        self.inputPath = "data"
        self.outputPath = "output/output.txt"
        self.timerPath = "output/timers.txt"
        self.expectedPath = "output/expected.txt"

        # files 
        self.fOutput = open(self.outputPath, 'w')
        self.fTimer = open(self.timerPath, 'w')

        self.getExpected()


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
        self.featuresLabled = []
        self.featuresTest = []

    

######################################################
#                READ FILES (TEST BY TEST)                            
######################################################
    def readFiles(self):
        count = 0
        ######################
        l = os.listdir(self.inputPath)
        l.sort()
        # print(l)
        # exit()
        # print(os.listdir(self.inputPath))
        # exit()
        ####################33
        # for test in os.listdir(self.inputPath):
        for test in l:
            if count == self.NumOfRuns:
                break
            count+=1
            
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
            self.Print()
            self.reinitialize()
            
        self.calculateAccuracy()



        # self.images   => [['data/01/1/1.png', 'data/01/1/2.png'], ['data/01/2/1.png', 'data/01/2/2.png'], ['data/01/3/1.png', 'data/01/3/2.png']]
        # self.writers  => [1, 2, 3]
        # self.tests    => ['data/01/test.png']


######################################################
#                    READ IMAGES                            
######################################################
    def readImages(self):
        for i in range(len(self.images)):
            for j in range(len(self.images[i])):
                self.images[i][j] = cv2.imread(self.images[i][j], 0)

        for i in range(len(self.tests)):
                self.tests[i] = cv2.imread(self.tests[i], 0)

    # self.images   => [['binary_image', 'binary_image'], ['binary_image', 'binary_image'], ['binary_image', 'binary_image']]
    # self.writers  => [1, 2, 3]
    # self.tests    => ['binary_image']

######################################################
#                START THE PIPELINE                            
######################################################
    def startPipeline(self):
        knn = KNeighborsClassifier(n_neighbors=1) # tune n_neighbors 
        Start = datetime.datetime.now()
        # The features of the labled data
        for i in self.images:
            # featuresList = []
            for j in i:
                _, preProcessing = preprocessing(j) #preprocessing.preprocessing(j) # Module => pre-processing, inputs => path of image 
                features = extractLBP(preProcessing) / (preProcessing.shape[0] * preProcessing.shape[1]) # Module => FS, inputs => pre-processed image
                # featuresList.append(features) 
                self.featuresLabled.append(features)

        Ytrain = [self.writers[0],self.writers[0],self.writers[1],self.writers[1],self.writers[2],self.writers[2]] 
        knn.fit(self.featuresLabled,Ytrain) 

        for i in self.tests:
            Start_pre = datetime.datetime.now()
            _, preProcessing = preprocessing(i) # Module => pre-processing, inputs => path of image 
            End_pre = datetime.datetime.now()

            Start_features = datetime.datetime.now()
            features = extractLBP(preProcessing) / (preProcessing.shape[0] * preProcessing.shape[1]) # Module => FS, inputs => pre-processed image
            End_features = datetime.datetime.now()
            self.featuresTest.append(features)

        
        output = knn.predict(self.featuresTest)   # Module => K-nn, inputs => self.featuresLabled, self.featuresTest, self.writers
                        # output => array of expected writers
                        # Now we assume that the output will be only one element and the test will be only one elment


        print("pre: ",(End_pre-Start_pre).total_seconds())
        print("features: ",(End_features-Start_features).total_seconds())
        End = datetime.datetime.now()
        self.output.extend(output)
        self.timers.append(str((End-Start).total_seconds()))
######################################################
#               GET EXPECTED OUTPUT  
######################################################
    def getExpected(self): 
        with open(self.expectedPath) as file_in:
            for line in file_in:
                self.expected.append(int(line.rstrip()))
######################################################
#               CALCULATE THE ACCURACY                            
######################################################
    def calculateAccuracy(self):

        if(len(self.expected) == 0):
            print("No expected output, no accuracy")

        if(len(self.expected) < len(self.output)):
            raise Exception("The number of expected output less than the actual number of output")
        count = 0
        for i in range(len(self.output)):
            if(self.expected[i] == self.output[i]):
                count+=1
        try:
            accuracy = (count/len(self.output))*100
        except ZeroDivisionError:
            print("Can't calculate the accuracy, the output list is empty")

        print("The accuracy is:",accuracy,"%")
        timerSum = 0
        for x in self.timers:
            timerSum += float(x)
        print("The average time is:",timerSum/len(self.timers))
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
        
        print("Identify the writer of ",self.testsPrint[0])
        print("The expected output is: ",self.expected[len(self.output)-1])
        print("The ectual output is: ",self.output[len(self.output)-1])
        print("=========================================================")

######################################################
#                 TEST FUNCTION  
######################################################
    def test(self):
        print(self.featuresLabled)
        print(self.featuresTest)
        print(self.writers)
        print(self.expected)
        print(self.output)
        print(self.images)
        print(self.tests)


######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    
    obj = i_o(10)
    obj.readFiles()
    
    
