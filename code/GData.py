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
        self.outputPath = "data"
        self.inputPath = "/home/sofyan/Downloads/Dataset"
        self.formText = "forms.txt"
        self.expectedPath = "output/expected.txt"
        self.currentTest = 0

        self.expectedFile = open(self.expectedPath, 'w')

        if(os.path.exists(self.outputPath)):
            shutil.rmtree(self.outputPath)
        os.mkdir(self.outputPath)

    def __del__(self):
        self.expectedFile.close()


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

        file_in.close()
######################################################
#               CREATE THE ARCHITECTURE                            
######################################################
    def createStructure(self): 
        
        if(self.numOfTests == self.currentTest):
            return True

        if(len(self.dic) == 3):
            self.write()
            self.currentTest+=1
            return False

        for i in self.form:
            if i not in self.dic and len(self.form[i]) > 2:
                self.dic[i] = self.form[i]
                if self.createStructure() is True:
                    return True

                lastElement = None
                for x in self.dic:
                    lastElement = x
                del self.dic[lastElement]

        return False


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
                    randImage = random.randint(2,len(self.dic[i])-1) # random image from third image to last image
                    copyfile(os.path.join(self.inputPath,self.dic[i][randImage]+".png"),os.path.join(path,self.dic[i][randImage]+".png"))
                    self.expectedFile.write(i+'\n') 
                    takeATest = 1
                if(imageCount > 2):
                    break
                copyfile(os.path.join(self.inputPath,j+".png"),os.path.join(path,i,j+".png"))

        

######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    n = input("The number of tests (Can't be more than 100 tests): ")

    obj = gData(int(n))
    obj.formTxt()
    obj.createStructure()
    
    
