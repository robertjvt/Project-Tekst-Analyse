# Exercise 1, assignment week 4
# Names: Robert van Timmeren, Kylian de rooij, Remi Thüss

import nltk
import os

def pos_tags(tokens):
    '''
    Returns a list of POS-tagged tokens from a list of tokens
    '''
    return nltk.pos_tag(tokens)

def main():
	for root, dirs, files in os.walk("group3", topdown=False):
	    for name in files:
	        if name == "en.tok.off":
	        	text = open(os.path.join(root, name)).readlines()
	        	f = open(os.path.join(root) + "/en.tok.off.pos", "w")
	        	tokens = []
	        	for line in text:
                        	line = line.rstrip()
                        	print(line)
                        	tokens.append(line.split()[3])
	        	print(tokens)
	        	pos_tags = nltk.pos_tag(tokens)
	        	print(pos_tags)
	        	for line in text:
                            output = line.rstrip() + ' ' + pos_tags[0][1] + '\n'
                            pos_tags.pop(0)
                            f.write(output)
                            print()
	        	f.close()
                        	

if __name__ == '__main__':
    main()
