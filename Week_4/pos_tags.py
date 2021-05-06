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
				for line in text:
					line = line.rstrip()
					word = line.split()[3]
					token = nltk.word_tokenize(word)
					pos_tagged = pos_tags(token)
					line = line + " " + pos_tagged[0][1]
					print(line)

if __name__ == '__main__':
    main()