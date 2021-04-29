# Exercise 1, assignment week 3
# Names: Robert van Timmeren, Kylian de rooij, Remi Thüss

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def pos_tags(tokens):
	'''
	Returns a list of POS-tagged tokens from a list of tokens
	'''
	return nltk.pos_tag(tokens)


def nouns_pos_tags(tagged_list):
	'''
	Returns a list of all nouns from a list of POS-tagged tokens
	'''
	noun_list = []
	for item in tagged_list:
		if item[1] == "NN" or item[1] == "NNP" or item[1] == "NNS":
			noun_list.append(item[0])
	return noun_list
	
def noun_lemmatize(noun_list):
	'''
	returns a list of lemmatized nouns from a list of nouns
	'''
	lem_nouns = []
	synset = ""
	for item in noun_list:
		lem_nouns.append(lemmatizer.lemmatize(item, wordnet.NOUN))
	return lem_nouns

def noun_synset(lem_nouns):
	'''
	returns a list of synsets of lemmatized nouns
	'''
	noun_synset = []
	for item in lem_nouns:
		noun_synset.append(wordnet.synsets(item, pos='n'))
	return noun_synset

def hypernymOf(synset1, synset2):
	""" 
	Returns True if synset2 is a hypernym of
	synset1, or if they are the same synset.
	Returns False otherwise. 
	"""
	print(synset1, synset2)
	if synset1 == synset2:
		return True
	for hypernym in synset1.hypernyms():
		if synset2 == hypernym:
			return True
		if hypernymOf(hypernym, synset2):
			return True
	return False

def hypernym_comparison(noun_synsets, words_compare):
	for synset in noun_synsets:
		if isinstance(synset, list):
			synset = synset[0]
		i = -1
		for word in words_compare:
			if isinstance(word, list):
				word = word[0]
			i += 1
			print(hypernymOf(word, synset))

def main():
	text = open('ada_lovelace.txt').read()
	tokens = nltk.word_tokenize(text)
	pos_tagged_list = pos_tags(tokens)
	noun_list = nouns_pos_tags(pos_tagged_list)
	lem_nouns = noun_lemmatize(noun_list)
	noun_synsets = noun_synset(lem_nouns)

	relative = wordnet.synsets("relative", pos='n')
	science = wordnet.synsets("science", pos='n')
	illness = wordnet.synsets("illness", pos='n')
	words_compare = [relative, science, illness]
	hypernym_comparison(noun_synsets, words_compare)

if __name__ == "__main__":
    main()