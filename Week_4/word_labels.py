import os 
import fnmatch

rootdir = 'group3/'

annotator1 = []
annotator2 = []
annotator3 = []
for root, dirs, files in os.walk("group3", topdown=False):
    for name in files:
        if name == "en.tok.off_Remi.txt":
            text1 = open(os.path.join(root, name)).readlines()
            for line in text1:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator1.append([linelist[3], linelist[5]])
                else:
                    annotator1.append([linelist[3], 'None'])
        elif name == "en.tok.off.pos.kylian":
            text2 = open(os.path.join(root, name)).readlines()
            for line in text2:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator2.append([linelist[3], linelist[5]])
                else:
                    annotator2.append([linelist[3], 'None'])
        elif name == "en.tok.off.pos.robert":
            text3 = open(os.path.join(root, name)).readlines()
            for line in text3:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator3.append([linelist[3], linelist[5]])
                else:
                    annotator3.append([linelist[3], 'None'])
for i in range(len(annotator1)):
    print(annotator1[i], annotator2[i], annotator3[i])




