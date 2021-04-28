import nltk
from collections import Counter


def pos_assist():
    sent = "Peter really liked the movies and warm pop-corn . He would never bring Mira with him, though .".split()
    wsj = nltk.corpus.brown.tagged_words()
    cfd1 = nltk.ConditionalFreqDist(wsj)
    for item in sent:
        print(item, cfd1[item].most_common())


def pos_tags_amount(br_tw):
    pos_tags = []
    for word in br_tw:
        if word[1] not in pos_tags:
            pos_tags.append(word[1])
    return len(pos_tags)


def top_15_tags(br_tw):
    pos_tags = {}
    for word in br_tw:
        if word[1] not in pos_tags:
            pos_tags[word[1]] = 1
        else:
            pos_tags[word[1]] += 1
    return sorted(pos_tags.items(), key=lambda x: x[1], reverse=True)[0:15]


def top_15_words(br_tw):
    words = {}
    for word in br_tw:
        if word[0] not in words:
            words[word[0]] = 1
        else:
            words[word[0]] += 1
    return sorted(words.items(), key=lambda x: x[1], reverse=True)[0:15]


def most_common_adverb(br_tw):
    adverb_preceders = [a for (a, b) in br_tw if b == 'RB']
    fdist = nltk.FreqDist(adverb_preceders)
    return fdist.most_common()[0]


def most_common_adj(br_tw):
    adj_preceders = [a for (a, b) in br_tw if b == 'JJ']
    fdist = nltk.FreqDist(adj_preceders)
    return fdist.most_common()[0]


def pos_so(br_tw):
    so = [b for (a, b) in br_tw if a == 'so']
    fdist = nltk.FreqDist(so)
    return fdist.most_common()


def so_sentences(br_ts):
    sentences = []
    types = ['QL', 'RB', 'CS']
    for sentence in br_ts:
        for (a, b) in sentence:
            if a == 'so' and b in types:
                sentences.append(sentence)
                types.remove(b)
    return sentences
        

def pos_preceding(br_tw):
    word_tag_pairs = nltk.bigrams(br_tw)
    so_preceders = [a[1] for (a, b) in word_tag_pairs if b[0] == 'so']
    fdist = nltk.FreqDist(so_preceders)
    return fdist.most_common()

    
def pos_following(br_tw):
    word_tag_pairs = nltk.bigrams(br_tw)
    so_preceders = [b[1] for (a, b) in word_tag_pairs if a[0] == 'so']
    fdist = nltk.FreqDist(so_preceders)
    return fdist.most_common()


def pos_tag(data):
    '''
    This function tags the entire text with appropriate POS tags.
    '''
    tokens = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokens)

    # Printing first 20 POS tags (full list is returned to main)
    print('\nFirst 20 POS tags')
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
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')
    
    print("{0}\nWords: {1}\nSentences: {2}".format("How many words and sentences are there?", len(br_tw), len(br_ts)))
    print("\n{0}\n{1}\n{2}".format("What is the 50th word and its POS? How about the 75th?", br_tw[49], br_tw[74]))
    print("\n{0}\n{1}".format("How many different POS tags are represented in this Brown category?", pos_tags_amount(br_tw)))
    print("\n{0}\n{1}".format("What are the top 15 POS tags and their counts?", top_15_tags(br_tw)))
    print("\n{0}\n{1}".format("What are the top 15 words and their counts?", top_15_words(br_tw)))
    print("\n{0}\n{1}\n{2}".format("What are the most frequent POS tag in the 20th sentence? And in the 40th?", top_15_tags(br_ts[19]), top_15_tags(br_ts[39])))
    print("\n{0}\n{1}".format("What is the most frequent adverb?", most_common_adverb(br_tw)))
    print("\n{0}\n{1}".format("What is the most frequent adjective?", most_common_adj(br_tw)))
    print("\n{0}\n{1}".format("What POS can the word 'so' be used for?", pos_so(br_tw)))    
    print("\n{0}\n{1}".format("What is the most frequent POS tag for 'so'?", pos_so(br_tw)[0]))
    print("\n{0}\n{1}".format("For each 'so' tag, give an example.", so_sentences(br_ts)))
    print("\n{0}\n{1}\n{2}".format("For each 'so's POS, find out the most likely preceding and following POS.", pos_preceding(br_tw)[0], pos_following(br_tw)[0]))
    # 3
    tagged = pos_tag(data)
    # 4
    pos_collocations(tagged)


if __name__ == '__main__':
    main()
