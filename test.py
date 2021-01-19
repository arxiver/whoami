# to decimal floating point (Done)

# the order of the directories


def sort(l):
    for i in range(len(l)):
        for j in range(len(l)):
            if int(l[i]) < int(l[j]):
                l[i],l[j] = l[j],l[i]

    return l

import os 

os.chdir("test")
l = sort(os.listdir("."))

print(l)