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
	        	for line in text:
                        	line = line.rstrip()
                        	token = line.split()[3]
                        	token = nltk.word_tokenize(token)
                        	pos_tag = nltk.pos_tag(token)
                        	output = line + ' ' + pos_tag[0][1] + '\n'
                        	f.write(output)
	        	f.close()
                        	

if __name__ == '__main__':
    main()
