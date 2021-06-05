import sys
import os
import wikipedia


def NE_features(data, i):
    '''
    Defines the features of all words in a dictionary.
    '''
    features = {
        'word': data[i][3],
        'POS': data[i][4],
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


def wiki_finder(data_features):    
    wiki_search = wikipedia.search(data[1])
    try:
        page = wikipedia.page(wiki_search[0])
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[0])

    print(page.url)
    return page.url


def main():
    with open('test.output') as file:
        data = []
        for line in file:
            line = line.rstrip().split()
            data.append(line)

    data_features = list_features(data)
    print(data_features)


if __name__ == '__main__':
    main()
