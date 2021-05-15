from collections import Counter
from nltk.metrics import ConfusionMatrix
import os


output = []
output2 = []
output3 = []

for root, dirs, files in os.walk("group3", topdown=False):
    for name in files:
        if name == 'en.tok.off.pos.robert':
            text1 = open(os.path.join(root, name)).readlines()
            for line in text1:
                line = line.split()
                if len(line) == 7:
                    output.append(line)
                else:
                    line.append('None')
                    line.append('None')
                    output.append(line)
        if name == 'en.tok.off.pos.kylian':
            text2 = open(os.path.join(root, name)).readlines()
            for line in text2:
                line = line.split()
                if len(line) == 7:
                    output2.append(line)
                else:
                    line.append('None')
                    line.append('None')
                    output2.append(line)
                    
        if name == 'en.tok.off_Remi.txt':
            text2 = open(os.path.join(root, name)).readlines()
            for line in text2:
                line = line.split()
                if len(line) == 7:
                    output3.append(line)
                else:
                    line.append('None')
                    line.append('None')
                    output3.append(line)   
i = 0
for item in output:
    item.append(output2[i][5])
    item.append(output2[i][6])
    i += 1
for item in output:
    print(item)


ref = 'DET NN VB DET JJ NN NN IN DET NN'.split()
tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
cm = ConfusionMatrix(ref, tagged)

print(cm)

labels = set('DET NN VB IN JJ'.split())

true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

for i in labels:
    for j in labels:
        if i == j:
            true_positives[i] += cm[i, j]
        else:
            false_negatives[i] += cm[i, j]
            false_positives[j] += cm[i, j]

print("TP:", sum(true_positives.values()), true_positives)
print("FN:", sum(false_negatives.values()), false_negatives)
print("FP:", sum(false_positives.values()), false_positives)
print()

for i in sorted(labels):
    if true_positives[i] == 0:
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i] +
                                              false_positives[i])
        recall = true_positives[i] / float(true_positives[i] +
                                           false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)
    print(i, fscore)
