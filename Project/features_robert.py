import sys
import os

from mediawiki import MediaWiki
import nltk
from nltk.corpus import wordnet


def NE_features(data, i):
    '''
    Defines the features of all words in a dictionary.
    '''
    features = {
        'word': data[i][3],
        'POS': data[i][4],
        'index': i
    }
    if len(data[i]) == 6:
        features.update({
            'NE': data[i][5]
        })

    if i > 0:
        features.update({
            'previous_word': data[i-1][3],
            'previous_POS': data[i-1][4],
        })
        
        if len(data[i-1]) == 6:
            features.update({
                'previous_NE': data[i-1][5]
        })
        
    if i < len(data) - 1:
        features.update({
            'next_word': data[i+1][3],
            'next_POS': data[i+1][4],
        })
        
        if len(data[i+1]) == 6:
            features.update({
                'next_NE': data[i+1][5]
        })

    return features


def list_features(data):
    '''
    Helper function with a list comprehension to loop through all words.
    '''
    return [NE_features(data, i) for i in range(len(data))]


def group_NE(DF):
    NE_length = 0
    NE_list = []
    for i in range(len(DF)):
        try:
            if DF[i]['NE']:
                NE_length += 1
                try:
                    if DF[i+1]['NE']:
                        continue
                except IndexError as e:
                    NNP = []
                    for j in range(NE_length):
                        NNP.append(DF[(i-NE_length+1)+j]['word'])
                    entity = ' '.join(NNP)
                    NE_list.append({
                        'entity': entity,
                        'NE': DF[i]['NE'],
                        'wiki': wiki_finder(entity),
                        'lower_index': i - NE_length + 1,
                        'upper_index': i
                    })
                except KeyError as e:
                    NNP = []
                    for j in range(NE_length):
                        NNP.append(DF[(i-NE_length+1)+j]['word'])
                    entity = ' '.join(NNP)
                    NE_list.append({
                        'entity': entity,
                        'NE': DF[i]['NE'],
                        'wiki': wiki_finder(entity),
                        'lower_index': i - NE_length + 1,
                        'upper_index': i
                    })
        except KeyError as e:
            NE_length = 0
    return NE_list


def wiki_finder(NE):    
    wikipedia = MediaWiki()
    wiki_search = wikipedia.search(NE)
    page = wikipedia.page(wiki_search[0])

    return page.url


def noun_finder(summary):
    sentence_tokens = nltk.sent_tokenize(summary)
    word_tokens = []
    noun_list = []
    for sentence in sentence_tokens:
        word_tokens.append(nltk.word_tokenize(sentence))
    for sentence in word_tokens:
        pos_tags = nltk.pos_tag(sentence)
        for tagged_word in pos_tags:
            if tagged_word[1][:2] == "NN":
                noun_list.append([tagged_word[0], sentence])
    return noun_list


def synset_finder(noun_list):
    synset_list = []
    for noun in noun_list:
        synsets = wordnet.synsets(noun[0], 'n')
        synset_list.append(synsets)
            
    

def find_wikipedia(NE):
    wikipedia = MediaWiki()
    possible_pages = wikipedia.search(NE)
    for item in possible_pages:
        page = wikipedia.page(item)
        summary = page.summary
        noun_list = noun_finder(summary)
        print(noun_list)
        

def main():
    with open('test.output') as file:
        data = []
        for line in file:
            line = line.rstrip().split()
            data.append(line)        
    data_features = list_features(data)
    NE_list = group_NE(data_features)
    
    for dictionary in NE_list:
        find_wikipedia(dictionary['entity'])
        

if __name__ == '__main__':
    main()
