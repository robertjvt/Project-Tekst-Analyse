from mediawiki import MediaWiki


def NE_features(NE_list, i):
    NE = NE_list[i]

    features = {
        'NE': NE
    }

    if i > 0:
        previous_NE = NE_list[i-1]
        features.update({
            'previous_NE': previous_NE,
        })
        
    if i < len(NE_list) - 1:
        next_NE = NE_list[i+1]
        features.update({
            'next_NE': next_NE,
        })
        
    return features
        


def list_features(NE_list):
    return [NE_features(NE_list, i) for i in range(len(NE_list))]



def wiki_finder(NE):
    wikipedia = MediaWiki()
    wiki_search = wikipedia.search(NE)
    page = wikipedia.page(wiki_search[0])
    return page.url


def main():
    NE_list = ['Obama', 'Facebook', 'Mexico', 'USA', 'KFC']

    X_train = list_features(NE_list)
    print(X_train)
    
    for NE in NE_list:
        url = wiki_finder(NE)
        print(url)




if __name__ == '__main__':
    main()
