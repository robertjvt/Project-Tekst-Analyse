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
    for line in fileinput.input():
        output = ""
        if ner_tags[0][1] == "COUNTRY" or ner_tags[0][1] == "STATE_OR_PROVINCE": 
            print(line.rstrip() + ' ' + "COU")
            #print(output)
        elif ner_tags[0][1] == "PERSON":
            print(line.rstrip() + ' ' + "PER")
        elif ner_tags[0][1] == "CITY":
            print(line.rstrip() + ' ' + "CIT")
        elif ner_tags[0][1] == "ORGANIZATION":
            print(line.rstrip() + ' ' + "ORG")
        elif ner_tags[0][1] == "ANI":
            print(line.rstrip() + ' ' + "ANI")
        elif ner_tags[0][1] == "NAT":
            print(line.rstrip() + ' ' + "NAT")
        elif ner_tags[0][1] == "SPO":
            print(line.rstrip() + ' ' + "SPO")
        #elif ner_tags[0][1] == "ENT":
        #    output = line.rstrip() + ' ' + "ENT" + '\n'
        else:
            print(line.rstrip())
        ner_tags.pop(0)
        #print(output)

def main():
    read_files()


if __name__ == '__main__':
    main()