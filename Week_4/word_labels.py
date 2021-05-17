import os
from nltk.metrics import ConfusionMatrix

annotator1 = []
annotator2 = []
annotator3 = []

ann_labels1 = []
ann_labels2 = []
ann_labels3 = []
for root, dirs, files in os.walk("group3", topdown=False):
    for name in files:
        if name == "en.tok.off_Remi.txt":
            text1 = open(os.path.join(root, name)).readlines()
            for line in text1:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator1.append([linelist[3], linelist[5]])
                    ann_labels1.append(linelist[5])
                else:
                    annotator1.append([linelist[3], 'None'])
                    ann_labels1.append('None')
        elif name == "en.tok.off.pos.kylian":
            text2 = open(os.path.join(root, name)).readlines()
            for line in text2:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator2.append([linelist[3], linelist[5]])
                    ann_labels2.append(linelist[5])
                else:
                    annotator2.append([linelist[3], 'None'])
                    ann_labels2.append('None')
        elif name == "en.tok.off.pos.robert":
            text3 = open(os.path.join(root, name)).readlines()
            for line in text3:
                linelist = line.split()
                if len(linelist) > 5:
                    annotator3.append([linelist[3], linelist[5]])
                    ann_labels3.append(linelist[5])
                else:
                    annotator3.append([linelist[3], 'None'])
                    ann_labels3.append('None')

'''for i in range(len(annotator1)):
    print(annotator1[i], annotator2[i], annotator3[i])'''

clean_labels1 = []
clean_labels2 = []
clean_labels3 = []
for i in range(len(ann_labels1)):
    #print(ann_labels1[i], ann_labels2[i], ann_labels3[i])
    if ann_labels1[i] != 'None' or ann_labels2[i] != 'None' or ann_labels3[i] != 'None':
        clean_labels1.append(ann_labels1[i])
        clean_labels2.append(ann_labels2[i])
        clean_labels3.append(ann_labels3[i])

'''for i in range(len(clean_labels1)):
    print(clean_labels1[i], clean_labels2[i], clean_labels3[i])'''

print(ConfusionMatrix(ann_labels1, ann_labels2))
print(ConfusionMatrix(clean_labels1, clean_labels2))

