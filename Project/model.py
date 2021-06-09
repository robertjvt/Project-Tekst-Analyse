#!/usr/bin/python3

import os

from nltk.parse import CoreNLPParser
from nltk.tag import StanfordNERTagger


def read_files():
    ner_tagger = CoreNLPParser(url='http://localhost:9001', tagtype='ner')

    
    for root, dirs, files in os.walk("dev", topdown=False):
        for name in files:
            if name == "en.tok.off.pos":
                print(os.path.join(root, name))
                text = open(os.path.join(root, name)).readlines()
                file = open(os.path.join(root) + "/en.tok.off.pos.ner", "w")
                tokens = []
                for line in text:
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
                    elif ner_tags[0][1] == "ENT":
                        output = line.rstrip() + ' ' + "ENT" + '\n'
                    else:
                        output = line.rstrip() + '\n'
                    ner_tags.pop(0)
                    #print(output)
                    file.write(output)
                file.close()              

def main():
    read_files()


main()