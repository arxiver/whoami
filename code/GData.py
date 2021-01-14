#!/home/sofyan/anaconda3/bin/python3
import os
from shutil import copyfile
import shutil
import random


class gData():
######################################################
#                       INIT                            
######################################################
    def __init__(self, n):
        self.numOfTests=n
        self.form = {}
        self.dic = {}
        self.outputPath = "data2"
        self.inputPath = "/home/sofyan/Downloads/Dataset"
        self.formText = "forms.txt"
        self.expectedPath = "output/expected.txt"
        self.currentTest = 0

        self.expectedFile = open(self.expectedPath, 'w')

        if(os.path.exists(self.outputPath)):
            shutil.rmtree(self.outputPath)
        os.mkdir(self.outputPath)


######################################################
#                   READ ALL IMAGES                            
######################################################
    def formTxt(self):
        with open(os.path.join(self.inputPath,self.formText)) as file_in:
            for line in file_in:
                if(line[0] != "#"):
                    if(line[0] == 'e'):
                        break
                    image = line.split(" ")[0]
                    writer = line.split(" ")[1]
                    if writer in self.form:
                        self.form[writer].append(image)
                    else:
                        self.form[writer] = [image]


######################################################
#               CREATE THE ARCHITECTURE                            
######################################################
    def createStructure(self): 
        
        for i in (self.form):
            if len(self.form[i]) > 2:
                self.dic[i] = self.form[i]
                if(len(self.dic) == 3):
                    self.write()
                    self.currentTest+=1


######################################################
#                       WRITE                            
######################################################
    def write(self):
        if(self.currentTest < 10):
            path = self.outputPath+"/00"+str(self.currentTest)
        elif(self.currentTest < 100):
            path = self.outputPath+"/0"+str(self.currentTest)
        elif(self.currentTest < 1000):
            path = self.outputPath+"/"+str(self.currentTest)
        else:
            raise Exception("The limit of tests is 1000")


        randomTest = random.randint(0,2)
        os.mkdir(path)
        writerCount = -1 
        takeATest = 0
        for i in self.dic:
            writerCount+=1
            if (os.path.exists(os.path.join(path, i))):
                shutil.rmtree(os.path.join(path, i))
            os.mkdir(os.path.join(path, i))

            imageCount = 0
            for j in self.dic[i]:
                imageCount+=1
                if(writerCount == randomTest and not takeATest):
                    copyfile(os.path.join(self.inputPath,self.dic[i][2]+".png"),os.path.join(path,self.dic[i][2]+".png"))
                    self.expectedFile.write(i+'\n') 
                    takeATest = 1
                if(imageCount > 2):
                    break
                copyfile("/home/sofyan/Downloads/Dataset/"+j+".png",path+"/"+i+"/"+j+".png")

        self.dic.clear()

######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    obj = gData(0)
    obj.formTxt()
    obj.createStructure()
    
    