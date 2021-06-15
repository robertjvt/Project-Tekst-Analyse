#!/usr/bin/python3

import sys
import os

from nltk.parse import CoreNLPParser
from nltk.tag import StanfordNERTagger

import fileinput


def read_files():
    ner_tagger = CoreNLPParser(url='http://localhost:9001', tagtype='ner')
    tokens = []
    for line in fileinput.input():
        line = line.rstrip()
        line = line.split()
        if len(line) == 6:
            tokens.append(line[4])
        else:
            tokens.append(line[3])
    ner_tags = ner_tagger.tag(tokens)
    ner_list = []
    for line in fileinput.input():
        output = ""
        if ner_tags[0][1] == "COUNTRY" or ner_tags[0][1] == "STATE_OR_PROVINCE": 
            ner_list.append(line.rstrip() + ' ' + "COU")
            #print(output)
        elif ner_tags[0][1] == "PERSON":
            ner_list.append(line.rstrip() + ' ' + "PER")
        elif ner_tags[0][1] == "CITY":
            ner_list.append(line.rstrip() + ' ' + "CIT")
        elif ner_tags[0][1] == "ORGANIZATION":
            ner_list.append(line.rstrip() + ' ' + "ORG")
        elif ner_tags[0][1] == "ANI":
            ner_list.append(line.rstrip() + ' ' + "ANI")
        elif ner_tags[0][1] == "NAT":
            ner_list.append(line.rstrip() + ' ' + "NAT")
        elif ner_tags[0][1] == "SPO":
            ner_list.append(line.rstrip() + ' ' + "SPO")
        #elif ner_tags[0][1] == "ENT":
        #    output = line.rstrip() + ' ' + "ENT" + '\n'
        else:
            ner_list.append(line.rstrip())
        ner_tags.pop(0)
        #print(output)
    return ner_list

def main():
    read_files()


if __name__ == '__main__':
    main()
