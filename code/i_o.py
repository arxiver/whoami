#!/home/sofyan/anaconda3/bin/python3
import os
import cv2
class i_o():
    def __init__(self,n):
        self.images = []
        self.writers = []
        self.featuresLabled = []
        self.featuresTest = []
        self.tests = []
        self.expected = []
        self.output = []
        self.accuracy = 0
        self.NumOfRuns = n
    
    def readFiles(self):
        path = "data"
        count = 0
        for test in os.listdir(path):
            if count == self.NumOfRuns:
                break
            self.NumOfRuns+=1
            
            for writer in os.listdir(os.path.join(path, test)):
                writerImages = []
                if "." in writer:
                    self.tests.append(os.path.join(path, test,writer))
                else:
                    for image in os.listdir(os.path.join(path, test,writer)):
                        writerImages.append(os.path.join(path, test,writer,image))
                    self.images.append(writerImages)
                    self.writers.append(int(writer))        # the name of the directory must be integer
            print(self.images)
            print(self.writers)
            print(self.tests)
            

    # self.images   => [['data/01/1/1.png', 'data/01/1/2.png'], ['data/01/2/1.png', 'data/01/2/2.png'], ['data/01/3/1.png', 'data/01/3/2.png']]
    # self.writers  => [1, 2, 3]
    # self.tests    => ['data/01/test.png']

    def readImages(self):
        for i in range(len(self.images)):
            for j in range(len(self.images[i])):
                self.images[i][j] = cv2.imread(self.images[i][j], 0)

        for i in range(len(self.tests)):
                self.tests[i] = cv2.imread(self.tests[i], 0)


    # self.images   => [['binary_image', 'binary_image'], ['binary_image', 'binary_image'], ['binary_image', 'binary_image']]
    # self.tests    => ['binary_image']


    def startPipeline(self):
        # The features of the labled data
        for i in self.images:
            featuresList = []
            for j in i:
                preProcessing = None # Module => pre-processing, inputs => path of image 
                features = None # Module => FS, inputs => pre-processed image
                featuresList.append(features) 
            self.featuresLabled.append(featuresList)

        for i in self.test:
            preProcessing = None # Module => pre-processing, inputs => path of image 
            features = None # Module => FS, inputs => pre-processed image
            self.featuresTest.append(features)

        output = None   # Module => K-nn, inputs => self.featuresLabled, self.featuresTest, self.writers
                        # output => array of expected writers

        self.output.extend(output)

        # self.output => [writer_test_1, writer_test_2, writer_test_3, etc...]

    def getExpected(self): 
        with open("output/expected.txt") as file_in:
            for line in file_in:
                self.expected.append(int(line.rstrip()))

        print(self.expected)

    def calculateAccuracy(self):
        count = 0
        for i in len(self.output):
            if(self.expected[i] == self.output[i]):
                count+=1
        
        self.accuracy = count/len(self.output)


    def writeOutput(self):
        f = open('output/output.txt', 'w') 
        f.writelines(self.output) 

if __name__ == "__main__":
    os.chdir("../")

    obj = i_o(1)
    obj.getExpected()
    obj.readFiles()
    obj.readImages()
    obj.startPipeline()
    obj.calculateAccuracy()
    obj.writeOutput()
    
