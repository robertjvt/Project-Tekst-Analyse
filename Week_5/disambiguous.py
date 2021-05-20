import wikipedia
from collections import Counter
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet


def noun_finder(content):
    '''
    This function finds all the nouns from a Wikipedia page and returns them
    in a list along with the corresponding sentence.
    '''
    sentence_list = []
    noun_list = []
    sent_tokens = sent_tokenize(content)
    for elem in sent_tokens:
        sentence_list.append(word_tokenize(elem))
    for sent in sentence_list:
        tagged_sent = pos_tag(sent)
        for word in tagged_sent:
            if word[1][:2] == 'NN':
                noun_list.append([word[0], sent])
    return noun_list


def print_1to4(noun_count, us_words, ps_words, total_ps_senses, sense_list):
    print('1. There were a total of {0} nouns in the text. {1} of those were unisemous and {2} were polysemous. The proportion of polysemous nouns is {3:.2f}.'.format(noun_count, us_words, ps_words, ps_words/noun_count))
    if ps_words == 1:
        print('2. This page contains a polysemous word.')
    elif ps_words == 0:
        print('2. This page does not contain any polysemous words.')
    elif ps_words > 1:
        print('2. This page contains multiple polysemous words.')
    print('3. The average number of senses per polysemous words is {0:.2f}'.format(total_ps_senses/ps_words))
    print('4. Count for different number of senses (format: nr of senses:count)')
    print(Counter(sense_list))


def synsets(noun_list):
    noun_count = 0
    ps_words = 0
    us_words = 0
    total_ps_senses = 0
    synset_list, sense_list, diff_senses = [], [], []
    for noun in noun_list:
        synsets = wordnet.synsets(noun[0], 'n')
        synset_list.append(synsets)
        if len(synsets) == 1:
            sense_list.append(len(synsets))
            noun_count += 1
            us_words += 1
        elif len(synsets) > 1:
            sense_list.append(len(synsets))
            noun_count += 1
            total_ps_senses += len(synsets)
            ps_words += 1
    print_1to4(noun_count, us_words, ps_words, total_ps_senses, sense_list)
    return synset_list


def main():
    wiki = wikipedia.page('Colonel Sanders')
    content = wiki.content
    noun_list = noun_finder(content)
    synset_list = synsets(noun_list)


if __name__ == '__main__':
    main()
