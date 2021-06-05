import sys
import os
from mediawiki import MediaWiki


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


def group_NE(DF):
    '''
    This function groups named entities by looking at the next words and their
    tags. It uses other functions to create a list of dictionaries
    (each dictionary containing features about the named entity).
    '''
    NE_length = 0
    NE_list = []
    for i in range(len(DF)):
        try:
            if DF[i]['NE']:
                NE_length += 1
                try:
                    if DF[i+1]['NE']:
                        if DF[i]['NE'] == DF[i+1]['NE']:
                            continue
                        else:
                            NE_list.append(entity_features(DF, i, NE_length))
                            NE_length = 0
                except IndexError as e:
                    NE_list.append(entity_features(DF, i, NE_length))
                    NE_length = 0
                except KeyError as e:
                    NE_list.append(entity_features(DF, i, NE_length))
                    NE_length = 0
        except KeyError as e:
            NE_length = 0
    return clean_list(NE_list)


def entity_features(DF, i, NE_length):
    '''
    This function creates a list of dictionaries for each named entity.
    It also checks whether there is a Wikipedia link, if there is not, the NE
    is ignored.
    '''
    NNP = []
    for j in range(NE_length):
        NNP.append(DF[(i-NE_length+1)+j]['word'])
    entity = ' '.join(NNP)
    url = wiki_finder(entity)
    if url is not None:
        features = {
            'entity': entity,
            'NE': DF[i]['NE'],
            'wiki': url,
            'lower_index': i - NE_length + 1,
            'upper_index': i
            }
        return features


def clean_list(NE_list):
    '''
    This function removes any instances of None in a list
    '''
    for i in range(len(NE_list)):
        if NE_list[i] is None:
            del NE_list[i]
    return NE_list


def wiki_finder(NE):
    '''
    This function takes a named entity, checks if there is a Wikipedia page
    for it and if so, returns the url.
    '''
    wikipedia = MediaWiki()
    wiki_search = wikipedia.search(NE)
    try:
        if wiki_search[0]:
            page = wikipedia.page(wiki_search[0])
            return page.url
    except IndexError as e:
        page = None
        return page


def main():
    with open('test.output') as file:
        data = []
        for line in file:
            line = line.rstrip().split()
            data.append(line)

    data_features = list_features(data)
    NE_list = group_NE(data_features)
    print(NE_list)


if __name__ == '__main__':
    main()
