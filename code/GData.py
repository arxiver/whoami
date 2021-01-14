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
        self.dec = {}
        self.directoryName = "data2"
        self.currentTest = 0
        self.path = "iam_database/forms.txt"
        self.f = open('output/expected.txt', 'w')


    def formTxt(self):
        with open(self.path) as file_in:
            for line in file_in:
                if(line[0] == 'e'):
                    break
                if(line[0] != "#"):
                    image = line.split(" ")[0]
                    writer = line.split(" ")[1]
                    if writer in self.form:
                        self.form[writer].append(image)
                    else:
                        self.form[writer] = [image]

        # count = -1
        # for i in self.form:
        #     count+=1
        #     if count == 20:
        #         break
        #     print(i,": ",end=''),
        #     for j in self.form[i]:
        #         print(j," ",end=''),

        #     print()
        #     print("=================")

        # exit()



    def createStructure(self): 
        if(os.path.exists(self.directoryName)):
            shutil.rmtree(self.directoryName)
        os.mkdir(self.directoryName)
        for i in (self.form):
            if len(self.form[i]) > 2:
                self.dec[i] = self.form[i]
                if(len(self.dec) == 3):
                    self.write()
                    self.currentTest+=1


    def write(self):
        if(self.currentTest < 10):
            path = self.directoryName+"/00"+str(self.currentTest)
        elif(self.currentTest < 100):
            path = self.directoryName+"/0"+str(self.currentTest)
        elif(self.currentTest < 1000):
            path = self.directoryName+"/"+str(self.currentTest)
        else:
            raise Exception("The limit of tests is 1000")


        test = random.randint(0,2)
        os.mkdir(path)
        count2 = -1
        takeATest = 0
        for i in self.dec:
            count2+=1 # index of writer
            if not (os.path.exists(path+"/"+i)):
                os.mkdir(path+"/"+i)
            count = 0
            
            for j in self.dec[i]:
                count+=1
                if(count2 == test and not takeATest):
                    copyfile("/home/sofyan/Downloads/Dataset/"+self.dec[i][2]+".png",path+"/"+self.dec[i][2]+".png")
                    self.f.write(i+'\n') 
                    takeATest = 1
                if(count > 2):
                    break
                copyfile("/home/sofyan/Downloads/Dataset/"+j+".png",path+"/"+i+"/"+j+".png")

        self.dec.clear()

######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    obj = gData(0)
    obj.formTxt()
    obj.createStructure()
    
    
