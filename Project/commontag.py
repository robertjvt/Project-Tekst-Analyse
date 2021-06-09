#!/usr/bin/python3

import os

def read_files():
    count = 0
    count_nat = 0
    count_ent = 0
    for root, dirs, files in os.walk("dev", topdown=False):
        for name in files:
            if name == "en.tok.off.pos.ent":
                print(os.path.join(root, name))
                text = open(os.path.join(root, name)).readlines()
                for line in text:
                    line = line.rstrip()
                    line = line.split()
                    if len(line) > 5:
                        if line[5] == "PER" or line[5] == "COU" or line[5] == "CIT" or line[5] == "ORG" or line[5] == "ANI" or line[5] == "SPO" or line[5] == "NAT" or line[5] == "ENT":
                            count += 1
                            if line[5] == "ENT":
                                count_ent += 1
                            if line[5] == "NAT":
                                count_nat += 1

    print("Total named entity tags: {0}".format(count))
    print("Number of NAT tags: {0} ({1}%)".format(count_nat, count_nat/count*100))
    print("Number of ENT tags: {0} ({1}%)".format(count_nat, count_ent/count*100))

def main():
    read_files()


main()