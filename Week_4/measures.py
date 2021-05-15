from collections import Counter
from nltk.metrics import ConfusionMatrix
import os

ref = 'DET NN VB DET JJ NN NN IN DET NN'.split()
tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
cm = ConfusionMatrix(ref, tagged)

print(cm)

labels = set('DET NN VB IN JJ'.split())

true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

for root, dirs, files in os.walk("group3", topdown=False):
      for name in files:
          if name == "en.tok.off_Remi.txt":
            text = open(os.path.join(root, name)).readlines()
            tokens = []

            annotated = []
            i = -1
            for line in text:
              i += 1
              line = line.rstrip()
              line = line.split()
              if len(line) == 7:
                annotated.append((i, line[5]))
            print(annotated)
          elif name == "en.tok.off.pos.kylian":
            print("Reading Kylian file")
          elif name == "en.tok.off.pos.robert":
            print("Reading robert file")

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
