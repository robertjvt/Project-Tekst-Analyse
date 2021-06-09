from mediawiki import MediaWiki


def NE_features(data, i):
    '''
    Defines the features of all words in a dictionary.
    '''

    # Adds word and its POS tag
    features = {
        'word': data[i][3],
        'POS': data[i][4],
    }

    # Adds the named entity tag
    if len(data[i]) == 6:
        features.update({
            'NE': data[i][5]
        })

    # Adds previous word and its POS tag
    if i > 0:
        features.update({
            'previous_word': data[i-1][3],
            'previous_POS': data[i-1][4],
        })

        # Adds previous named entity tag
        if len(data[i-1]) == 6:
            features.update({
                'previous_NE': data[i-1][5]
            })

    # Adds next word and its POS tag
    if i < len(data) - 1:
        features.update({
            'next_word': data[i+1][3],
            'next_POS': data[i+1][4],
        })

        # Adds the next named entity tag
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
            # If this word is a named entity
            if DF[i]['NE']:
                NE_length += 1
                try:
                    # If the next word is a NE
                    if DF[i+1]['NE']:
                        # If the next NE has the same tag as the current NE.
                        if DF[i]['NE'] == DF[i+1]['NE']:
                            continue
                        else:
                            NE_list.append(entity_features(DF, i, NE_length))
                            NE_length = 0
                # IndexError means that this is the end of the list and there
                # are more elements after the current one.
                except IndexError:
                    NE_list.append(entity_features(DF, i, NE_length))
                    NE_length = 0
                # KeyError means that the next element is not a NE as it does
                # not have that key.
                except KeyError:
                    NE_list.append(entity_features(DF, i, NE_length))
                    NE_length = 0
        # KeyError means that the current element is not a NE.
        except KeyError:
            NE_length = 0

    return clean_list(NE_list)


def entity_features(DF, i, NE_length):
    '''
    This function creates a list of dictionaries for each named entity.
    It also checks whether there is a Wikipedia link, if there is not, the NE
    is ignored.
    '''
    entity = []
    for j in range(NE_length):
        # Adds all words belonging to this entity to a list
        entity.append(DF[(i - NE_length + 1) + j]['word'])
    # Makes entity into a string
    entity = ' '.join(entity)
    url = wiki_finder(entity)
    # If there is a url, create a dictionary with features
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
        # If the wiki search has any results
        if wiki_search[0]:
            page = wikipedia.page(wiki_search[0])
            return page.url
    # IndexError means that the search did not find any results
    except IndexError:
        return


def file_generator(data, NE_list):
    '''
    This function prints the data to an output file.
    '''
    with open('test.output.ent', 'w') as outfile:
        for i in range(len(data)):
            try:
                # Setting variables
                lower_i = NE_list[0]['lower_index']
                upper_i = NE_list[0]['upper_index']
                line = ' '.join(data[i][0:5]) + '\n'
                line_NE = ' '.join(data[i][0:5]) + ' ' + NE_list[0]['NE'] + ' ' + NE_list[0]['wiki'] + '\n'

                # The program checks the index of the current iteration with
                # the indeces given in the dictionary, based on this, the
                # program can see if the word is a NE and thus needs a
                # different output.
                if i == lower_i:
                    outfile.write(line_NE)
                    if i < upper_i:
                        continue
                    elif i == upper_i:
                        del NE_list[0]
                elif i > lower_i and i < upper_i:
                    outfile.write(line_NE)
                elif i == upper_i:
                    outfile.write(line_NE)
                    del NE_list[0]
                elif i < lower_i:
                    outfile.write(line)
            # IndexError means there are no more NE left, but as long as the
            # iteration is happening, it prints the line
            except IndexError:
                line = ' '.join(data[i][0:5]) + '\n'
                outfile.write(line)


def main():
    with open('test.output') as file:
        data = []
        for line in file:
            line = line.rstrip().split()
            data.append(line)

    data_features = list_features(data)
    NE_list = group_NE(data_features)
    file_generator(data, NE_list)


if __name__ == '__main__':
    main()
