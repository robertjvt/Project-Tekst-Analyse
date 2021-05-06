# Exercise 1, assignment week 4
# Names: Robert van Timmeren, Kylian de rooij, Remi Thüss

import nltk
import os

def main():
	for root, dirs, files in os.walk("group3", topdown=False):
	    for name in files:
	        if name == "en.tok.off":
	            

if __name__ == '__main__':
    main()