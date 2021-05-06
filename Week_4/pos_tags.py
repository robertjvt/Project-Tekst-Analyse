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
	        	text = open(os.path.join(root, name)).read()
	        	

	        	#tokens = nltk.word_tokenize(text)
	        	#pos_tagged_list = pos_tags(tokens)
	        	#print(pos_tagged_list)

if __name__ == '__main__':
    main()