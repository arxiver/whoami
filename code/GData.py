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
        self.outputPath = "/mnt/sda9/sda5/data1"
        self.inputPath = "Dataset"
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


        # remove all writer has less than 3 images
        for i in list(self.form):
            if(len(self.form[i]) < 3):
                del self.form[i]


        # pick a random writer
        
        # test = random.choice(list(self.form.keys()))
        # print(test)


        # Print all writer and their images

        # count = 0
        # for i in self.form:
        #     if(len(self.form[i]) > 2):
        #         count+=1
        #     print(i,"=> ", end="")
        #     for j in self.form[i]:
        #         print(j," ",end=" ")
        #     print()
        #     print("==================")
        # print(count)

        
######################################################
#               CREATE THE ARCHITECTURE                            
######################################################
    def createStructure(self): 
        
        # Generate all compination
        ##############################
        # if(self.numOfTests == self.currentTest):
        #     return True

        # if(len(self.dic) == 3):
        #     self.write()
        #     self.currentTest+=1
        #     return False

        # for i in self.form:
        #     if i not in self.dic and len(self.form[i]) > 2:
        #         self.dic[i] = self.form[i]
        #         if self.createStructure() is True:
        #             return True

        #         lastElement = None
        #         for x in self.dic:
        #             lastElement = x
        #         del self.dic[lastElement]

        # return False
        #####################################################


        for i in range(0,self.numOfTests):
            w1 = random.choice(list(self.form.keys()))

            w2 = random.choice(list(self.form.keys()))
            while(w2 == w1):
                w2 = random.choice(list(self.form.keys()))

            w3 = random.choice(list(self.form.keys()))
            while(w3 == w2 or w3 == w1):
                w3 = random.choice(list(self.form.keys()))

            self.dic[w1] = self.form[w1]
            self.dic[w2] = self.form[w2]
            self.dic[w3] = self.form[w3]
            self.write()
            self.currentTest+=1
            self.dic.clear()

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
            path = self.outputPath+"/"+str(self.currentTest)
            # raise Exception("The limit of tests is 1000")


        randomTest = random.randint(0,2)
        os.mkdir(path)
        writerCount = -1 
        takeATest = 0
        for i in self.dic:
            writerCount+=1
            if (os.path.exists(os.path.join(path, i))):
                shutil.rmtree(os.path.join(path, i))
            os.mkdir(os.path.join(path, i))


            copyList = self.dic[i].copy()
            imageCount = 0
            while imageCount < 2:
                imageCount+=1

                randImage = random.randint(0,len(copyList)-1)
                imageName = copyList.pop(randImage)+".png"
                copyfile(os.path.join(self.inputPath,imageName),os.path.join(path,i,imageName))

                if(writerCount == randomTest and not takeATest):
                    randImage = random.randint(0,len(copyList)-1)
                    imageName = copyList.pop(randImage)+".png"
                    copyfile(os.path.join(self.inputPath,imageName),os.path.join(path,imageName))
                    self.expectedFile.write(i+'\n') 
                    takeATest = 1
        

######################################################
#                       MAIN                            
######################################################
if __name__ == "__main__":
    os.chdir("../")

    n = input("The number of tests (It's better not to exceed 1000): ")

    obj = gData(int(n))
    obj.formTxt()
    obj.createStructure()
    
    
