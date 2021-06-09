import sys
import os

from mediawiki import MediaWiki
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from collections import Counter


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
                        #'wiki': wiki_finder(entity),
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
                        #'wiki': wiki_finder(entity),
                        'lower_index': i - NE_length + 1,
                        'upper_index': i
                    })
        except KeyError as e:
            NE_length = 0
    return NE_list


def best_match(final_pages, label):
    best_count = 0
    best_page = ''
    
    for item in final_pages:
        summary = [word.lower() for word in item[1].split()]
        count = 0

        if label == 'COU':
            keywords = ['country', 'state', 'province', 'county']
            for keyword in keywords:
                if keyword in summary:
                    count += 1
        
        elif label == 'CIT':
            keywords = ['city', 'town', 'place']
            for keyword in keywords:
                if keyword in summary:
                    count += 1
                    
        elif label == 'NAT':
            keywords = ['mountain', 'river', 'ocean', 'lake', 'volcano', 'sea', 'forest', 'natural']
            for keyword in keywords:
                if keyword in summary:
                    count += 1
            
        elif label == 'PER':
            keywords = ['born', 'he', 'she', 'person', 'was', 'is', 'father', 'mother']
            for keyword in keywords:
                if keyword in summary:
                    count += 1
                    
        elif label == 'ORG':
            keywords = ['organization', 'company', 'profit', 'founded', 'headquarters']
            for keyword in keywords:
                if keyword in summary:
                    count += 1

        elif label == 'ANI':
            keywords = ['domestic', 'descendent', 'animal', 'breed', 'species', 'specy']
            for keyword in keywords:
                if keyword in summary:
                    count += 1

        elif label == 'SPO':
            keywords = ['sport', 'team', 'football', 'soccer', 'baseball', 'basketball', 'sports', 'players']
            for keyword in keywords:
                if keyword in summary:
                    count += 1

        if count > best_count:
            best_page = item
            best_count = count
    return best_page[2]


def find_wikipedia(dictionary):
    wikipedia = MediaWiki()
    NE = dictionary['entity']
    label = dictionary['NE']
    possible_pages = wikipedia.search(NE)
    final_pages = []
    
    for item in possible_pages:
        try:
            page = wikipedia.page(item)
            summary = page.summarize()
            url = page.url
            final_pages.append([page, summary, url])
        except Exception as e:
            options = e.options

    return best_match(final_pages, label)


def main():
    with open('test.output') as file:
        data = []
        for line in file:
            line = line.rstrip().split()
            data.append(line)        
    data_features = list_features(data)
    NE_list = group_NE(data_features)

    for dictionary in NE_list:
        dictionary['wiki_link'] = find_wikipedia(dictionary)

    print(NE_list)
        
        

if __name__ == '__main__':
    main()
