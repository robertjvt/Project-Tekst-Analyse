# Exercise 1, assignment week 3
# Names: Robert van Timmeren, Kylian de rooij, Remi Thüss

import nltk
import re
from operator import itemgetter
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
		if len(wordnet.synsets(item, pos='n')) > 0:
			noun_synset.append(wordnet.synsets(item, pos='n'))
	return noun_synset


def hypernymOf(synset1, synset2):
	""" 
	Returns True if synset2 is a hypernym of
	synset1, or if they are the same synset.
	Returns False otherwise. 
	"""
	if synset1 == synset2:
		return True
	for hypernym in synset1.hypernyms():
		if synset2 == hypernym:
			return True
		if hypernymOf(hypernym, synset2):
			return True
	return False


def hypernym_comparison(noun_synsets, words_compare):
	'''
	Compares a list of synsets to another lists of synsets to look
	for references and prints the words and the references.
	'''
	for synset in noun_synsets:
		if isinstance(synset, list):
			synset = synset[0]
		for word in words_compare:
			if isinstance(word, list):
				word = word[0]
			if hypernymOf(word, synset) == True:
				word = re.sub(r'(Synset\()\'(.*?)(.n.01)\'(\))', r'\2' ,str(word))
				reference = re.sub(r'(Synset\()\'(.*?)(.n.01)\'(\))', r'\2' ,str(synset))
				print("{0} --> {1}".format(word, reference))


def similarity(syn_list_1, syn_list_2):
	'''
	For 2 lists of synsets of words returns a list of their similarity
	'''
	i = -1
	sim = []
	for syn in syn_list_1:
		i += 1
		if isinstance(syn, list):
			syn = syn[0]
		if isinstance(syn_list_2[i], list):
			syn_list_2[i] = syn_list_2[i][0]
			sim.append(syn.wup_similarity(syn_list_2[i]))
	return sim


def sort_list(li1, li2, li3):
	'''
	Combines 3 lists into tuples into a new and sorted lists
	where li1[0], li2[0], li3[0] are: [(li1[0], li2[0], li3[0])]
	'''
	i = -1
	wordlist = []
	for item in li1:
		i += 1
		tuples = (item, li2[i], li3[i])
		wordlist.append(tuples)
	wordlist.sort(key=itemgetter(2), reverse=True)
	return wordlist


def main():
    text = open('ada_lovelace.txt').read()
    tokens = nltk.word_tokenize(text)
    pos_tagged_list = pos_tags(tokens)
    noun_list = nouns_pos_tags(pos_tagged_list)
    lem_nouns = noun_lemmatize(noun_list)
    noun_synsets = noun_synset(lem_nouns)

    
    words = ['automobile', 'coast']
    words2 = ['car', 'shore']
    print(similarity(noun_synset(words), noun_synset(words2)))


    print(similarity(noun_synset(['chiefly']), noun_synset(['location'])))





if __name__ == "__main__":
    main()
