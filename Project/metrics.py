#!/usr/bin/python3

import sys
import os
from nltk.metrics import ConfusionMatrix
from sklearn.metrics import classification_report


def open_files():
    output = []
    golden = []
    for root, dirs, files in os.walk("dev", topdown=False):
        for name in files:
            if name == "en.tok.off.pos.ent.output":
                file = open(os.path.join(root, name)).readlines()
                for line in file:
                    line = line.rstrip().split()
                    if len(line) > 5 and line[5] == '-':
                        line.pop(5)
                    if len(line) > 6 and line[6] == '-':
                        line.pop(6)
                    output.append(line)
            if name == "en.tok.off.pos.ent":
                file = open(os.path.join(root, name)).readlines()
                for line in file:
                    line = line.rstrip().split()
                    if len(line) > 5 and line[5] == '-':
                        line.pop(5)
                    if len(line) > 6 and line[6] == '-':
                        line.pop(6)
                    golden.append(line)
    return output, golden


def clean_labels(l1, l2):
    '''
    This function clears the labels from instances where both lists have
    'None' at the same index.
    '''
    cl1, cl2 = [], []
    for i in range(len(l1)):
        if l1[i] != 'None' or l2[i] != 'None':
            cl1.append(l1[i])
            cl2.append(l2[i])
    return cl1, cl2


def clean_bool_labels(bl1, bl2):
    '''
    This function clears the boolean labels from instances where both lists
    have 'False' at the same index.
    '''
    cblt1, cblt2 = [], []
    cblf1, cblf2 = [], []
    for i in range(len(bl1)):
        if bl1[i] == 'True' or bl2[i] == 'True':
            cblt1.append(bl1[i])
            cblt2.append(bl2[i])
    for i in range(len(bl1)):
        if bl1[i] == 'False' or bl2[i] == 'False':
            cblf1.append(bl1[i])
            cblf2.append(bl2[i])
    return cblt1, cblt2, cblf1, cblf2


def give_label(root, name, anno, labels, bool_labels):
    '''
    This function parses through a file and gives it labels where appropriate.
    '''
    with open(os.path.join(root, name)) as f:
        text = f.readlines()
    for line in text:
        linelist = line.split()
        if len(linelist) > 6 and linelist[6] == '-':
            linelist.pop(6)
        if len(linelist) > 5 and linelist[5] == '-':
            linelist.pop(5)
        # If the linelist is longer than 5, there is an annotation
        if len(linelist) > 5 and linelist[3]:
            anno.append([linelist[3], linelist[5]])
            labels.append(linelist[5])
            bool_labels.append('True')
        # If the linelist is not longer than 5, there is no annotation
        else:
            anno.append([linelist[3], 'None'])
            labels.append('None')
            bool_labels.append('False')
    
    return anno, labels, bool_labels


def word_labels(file1, file2):
    '''
    This function uses other functions to parse the annotated files and
    create lists with the words and their corresponding labels.
    '''
    # anno is usually not used, but if was found useful when adjudicating
    # anno includes word and its assigned label
    anno1, anno2 = [], []
    # labels only includes the label
    labels1, labels2 = [], []
    # bool_labels includes 'True' and 'False' depending on whether there is a
    # label present
    bool_labels1, bool_labels2 = [], []
    
    # This iterates through the directories and files
    for root, dirs, files in os.walk("dev_metrics", topdown=False):
        for name in files:
            # If the name is the same as the first file input into the
            # program
            if name == file1:
                anno1, labels1, bool_labels1 = give_label(root, name, anno1, labels1, bool_labels1)
                #print(labels1)
            # If the name is the same as the second file input into the
            # program
            elif name == file2:
                anno2, labels2, bool_labels2 = give_label(root, name, anno2, labels2, bool_labels2)
    return labels1, labels2, bool_labels1, bool_labels2


def print_agreement(cl1, cl2, cblt1, cblt2, cblf1, cblf2):
    '''
    This function prints two classification reports and a confusion matrix
    '''
    print('Agreement on finding interesting entities:')
    print(classification_report(cblt1, cblt2, digits=3))
    print('Agreement on finding uninteresting entities:')
    print(classification_report(cblf1, cblf2, digits=3))
    print('Agreement on classifying entities:')
    print(classification_report(cl1, cl2, digits=3))
    print('Confusion matrix:')
    print(ConfusionMatrix(cl1, cl2))


def measure_wiki(output, golden):
    output_wiki = []
    golden_wiki = []
    
    for i in range(len(output)):
        if len(output[i]) > 6 and len(golden[i]) > 6:
            output_wiki.append(output[i][6])
            golden_wiki.append(golden[i][6])
    acc = 0
    total = len(golden_wiki)

    for i in range(len(output_wiki)):
        if output_wiki[i] == golden_wiki[i]:
            acc += 1

    print('Accuracy wikification:', acc / total)
    

def main(file1, file2):
    labels1, labels2, bool_labels1, bool_labels2, = word_labels(file1, file2)
    cl1, cl2 = clean_labels(labels1, labels2)
    cblt1, cblt2, cblf1, cblf2 = clean_bool_labels(bool_labels1, bool_labels2)
    print_agreement(cl1, cl2, cblt1, cblt2, cblf1, cblf2)
    output, golden = open_files()
    measure_wiki(output, golden)


if len(sys.argv) != 3:
    print('Error:')
    print('This program takes two positional arguments, {0} were given'.format(len(sys.argv)-1))
    print('Please use the following format:')
    print('python3 test2.py [filename 1] [filename 2]')
    exit()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
