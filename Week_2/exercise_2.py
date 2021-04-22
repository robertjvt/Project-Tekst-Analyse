import nltk
from collections import Counter


def pos_tag(data):
    '''
    This function tags the entire text with appropriate POS tags.
    '''
    tokens = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokens)

    # Printing first 20 POS tags (full list is returned to main)
    print('First 20 POS tags')
    for i in range(20):
        print(tagged[i])
    print('...', '\n')
    return tagged


def create_pos_text(tagged):
    '''
    This function creates a text/string containing all the pos tags, which can
    be used by pos_collocations() for calculations.
    '''
    pos_text = ''
    for element in tagged:
        pos_text += element[1] + ' '
    return pos_text


def pos_collocations(tagged):
    '''
    This function calculates the raw frequency of POS tag bigrams and
    the PMI scores of POS collocations. It prints the top 5 of each
    respectively.
    '''
    pos_text = create_pos_text(tagged)
    pos_tokens = nltk.word_tokenize(pos_text)

    # Calculating raw frequencies of POS tag bigrams
    pos_bigram_count = Counter(list(nltk.bigrams(pos_tokens))).most_common(5)

    # Calculating PMI scores of POS collocations
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = nltk.BigramCollocationFinder.from_words(pos_tokens)
    score_list = []
    for i in finder.score_ngrams(bigram_measures.pmi):
        score_list.append(i)

    # Printing PMI scores and raw frequencies
    # (full lists are returned to main)
    print('Top 5 PMI scores:')
    for i in range(5):
        print(score_list[i])
    print()
    print('Top 5 raw frequencies:')
    for element in pos_bigram_count:
        print(element)

    return score_list, pos_bigram_count


def main():
    with open('holmes.txt') as file:
        data = file.read()
    # 3
    tagged = pos_tag(data)
    # 4
    pos_collocations(tagged)


if __name__ == '__main__':
    main()
