#!/home/sofyan/anaconda3/bin/python3
import os
import cv2
from preprocessing import preprocessing
from featureExtraction import extractLBP

import datetime

class i_o():

######################################################
#                       INIT                            
######################################################
    def __init__(self, n):
        self.images = []
        self.writers = []
        self.featuresLabled = []
        self.featuresTest = []
        self.tests = []
        self.expected = []
        self.output = []
        self.timers = []
        self.imagesPrint = []
        self.accuracy = 0
        self.NumOfRuns=n
        self.path = "data"

        self.getExpected()


######################################################
#                       RE-INIT                            
######################################################
    def reinitialize(self):
        self.images = []
        self.imagesPrint = []
        self.writers = []
        self.featuresLabled = []
        self.featuresTest = []
        self.tests = []
        self.accuracy = 0
    

######################################################
#                READ FILES (TEST BY TEST)                            
######################################################
    def readFiles(self):
        count = 0
        for test in os.listdir(self.path):
            if count == self.NumOfRuns:
                break
            count+=1
            
            for writer in os.listdir(os.path.join(self.path, test)):
                writerImages = []
                writerImagesPrint = []
                if "." in writer:
                    self.tests.append(os.path.join(self.path, test,writer))
                else:
                    for image in os.listdir(os.path.join(self.path, test,writer)):
                        writerImages.append(os.path.join(self.path, test,writer,image))
                        writerImagesPrint.append(os.path.join(self.path, test,writer,image))
                    self.images.append(writerImages)
                    self.imagesPrint.append(writerImagesPrint)
                    self.writers.append(int(writer))        # the name of the directory must be integer

            # self.test()
            # exit()

            self.readImages()
            self.startPipeline()
            self.calculateAccuracy()
            self.writeOutput()
            self.reinitialize()
            self.Print()
            

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
        Start = datetime.datetime.now()
        # The features of the labled data
        for i in self.images:
            featuresList = []
            for j in i:
                preProcessing = None #preprocessing.preprocessing(j) # Module => pre-processing, inputs => path of image 
                features = None # Module => FS, inputs => pre-processed image
                featuresList.append(features) 
            self.featuresLabled.append(featuresList)

        for i in self.tests:
            preProcessing = None # Module => pre-processing, inputs => path of image 
            features = None # Module => FS, inputs => pre-processed image
            self.featuresTest.append(features)

        output = []   # Module => K-nn, inputs => self.featuresLabled, self.featuresTest, self.writers
                        # output => array of expected writers
                        # Now we assume that the output will be only one element and the test will be only one elment

        End = datetime.datetime.now()
        self.output.extend(output)
        self.timers.append(str((End-Start).total_seconds()))

        # self.output => [writer_test_1, writer_test_2, writer_test_3, etc...]
######################################################
#               GET EXPECTED OUTPUT  
######################################################
    def getExpected(self): 
        with open("output/expected.txt") as file_in:
            for line in file_in:
                self.expected.append(int(line.rstrip()))

        print(self.expected)


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
            self.accuracy = count/len(self.output)
        except ZeroDivisionError:
            print("Can't calculate the accuracy, the output list is empty")


######################################################
#                WRITE THE OUTPUT  
######################################################
    def writeOutput(self):
        f = open('output/output.txt', 'w') 
        f.writelines(self.output) 

        f = open('output/timers.txt', 'w') 
        f.writelines(self.timers) 


######################################################
#                       PRINT         
######################################################

    # Assumtion: The len of tests and output is 1
    
    def Print(self):
        if(len(self.tests) == 0 or len(self.output) == 0):
            raise Exception("The lenght of tests or output is zero, wrong")
        for i in self.imagesPrint:
            for j in i:
                print("processing ",j,"....")

        print("Identify the writer of ",self.tests[0]," => ",self.output[len(self.output-1)])

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

    obj = i_o(1)
    obj.readFiles()
    
    
