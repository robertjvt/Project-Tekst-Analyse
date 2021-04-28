import nltk
from nltk.collocations import *
from nltk.metrics.spearman import *

def top_bigrams_pmi(tokens):
    ''' 
    Returns the top 20 bigrams in a supplied tokenized text using PMI (no filter).
    '''
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(2)
    # The filter below can be uncommented to exclude collocations that occur < 3 times.
        
    # finder.apply_freq_filter(3)
    return sorted(finder.nbest(bigram_measures.pmi, 20))


def top_bigrams_chi(tokens):
    ''' 
    Returns the top 20 bigrams in a supplied tokenized text using chi squared (no filter).
    '''
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(2)

    return sorted(finder.nbest(bigram_measures.chi_sq, 20))


def top_bigrams_raw(tokens):
    ''' 
    Returns the top 20 bigrams in a supplied tokenized text 
    without using any association measure
    '''
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    sorted_bigrams = [bigram for bigram, _ in sorted(scored, key=lambda x: x[1], reverse=True)]

    return sorted_bigrams[0:20]


def spearman_cooficient(rank_list_1, rank_list_2):
    '''
    Returns the spearman spearman coefficient of 2 lists
    '''
    return spearman_correlation(ranks_from_sequence(rank_list_1),ranks_from_sequence(rank_list_2))


def main():
    text = open('holmes.txt').read()
    tokens = nltk.wordpunct_tokenize(text)

    print("\n1a:\n")
    print(top_bigrams_pmi(tokens))

    print("\n1b:\n")
    print(top_bigrams_chi(tokens))

    print("\n1c:\n")
    print(top_bigrams_raw(tokens))
    print("\nExplanation: PMI measures how often a bigram appears in relation to its unigrams. "
        "Chi-square measures how likely it is that a bigram appears but also how often it doesn't  "
        "appear in relation to the expected amount. This can (and in this case does) lead to slightly different results")

    print("\n1d:\n")
    print("Spearman’s coefficient: " + 
        str(spearman_cooficient(top_bigrams_pmi(tokens), top_bigrams_chi(tokens))))

if __name__ == "__main__":
    main()

