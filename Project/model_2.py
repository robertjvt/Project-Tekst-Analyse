#!/usr/bin/python3

import sys
import os

from nltk.parse import CoreNLPParser
from nltk.tag import StanfordNERTagger


def read_files(argv):
    ner_tagger = CoreNLPParser(url='http://localhost:9001', tagtype='ner')
    text = sys.stdin.readlines()
    tokens = []
    for line in text:
        sys.stdout.write(line)
        line = line.rstrip()
        line = line.split()
        if len(line) == 6:
            tokens.append(line[4])
        else:
            tokens.append(line[3])
    ner_tags = ner_tagger.tag(tokens)
    for line in text:
        output = ""
        if ner_tags[0][1] == "COUNTRY" or ner_tags[0][1] == "STATE_OR_PROVINCE": 
            output = line.rstrip() + ' ' + "COU" + '\n'
            #print(output)
        elif ner_tags[0][1] == "PERSON":
            output = line.rstrip() + ' ' + "PER" + '\n'
        elif ner_tags[0][1] == "CITY":
            output = line.rstrip() + ' ' + "CIT" + '\n'
        elif ner_tags[0][1] == "ORGANIZATION":
            output = line.rstrip() + ' ' + "ORG" + '\n'
        elif ner_tags[0][1] == "ANI":
            output = line.rstrip() + ' ' + "ANI" + '\n'
        elif ner_tags[0][1] == "NAT":
            output = line.rstrip() + ' ' + "NAT" + '\n'
        elif ner_tags[0][1] == "SPO":
            output = line.rstrip() + ' ' + "SPO" + '\n'
        #elif ner_tags[0][1] == "ENT":
        #    output = line.rstrip() + ' ' + "ENT" + '\n'
        else:
            sys.stdout.write(line.rstrip() + '\n')
        ner_tags.pop(0)
        #print(output)
        file.write(output)
    file.close()

def main(argv):
    read_files(argv)


if __name__ == '__main__':
    main(sys.argv[1])