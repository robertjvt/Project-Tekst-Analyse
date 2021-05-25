import wikipedia
from collections import Counter
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.wsd import lesk


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


def synsets(noun_list):
    '''
    Finds all corresponding synsets and their senses to the nouns, tracks the amount of nouns and
    whether they are unisemous or polysemous.
    '''
    noun_count = 0
    ps_words = 0
    us_words = 0
    total_ps_senses = 0
    words_10 = 0
    nouns_list = []
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
            if words_10 < 10:
              nouns_list.append(noun)
              words_10 += 1
    return synset_list, nouns_list, noun_count, us_words, ps_words, total_ps_senses, sense_list
  

def main():
    wiki = wikipedia.page('Colonel Sanders')
    content = wiki.content
    noun_list = noun_finder(content)
    synset_list, first_nouns, noun_count, us_words, ps_words, total_ps_senses, sense_list = synsets(noun_list)
    
    print('1.\nThere were a total of {0} nouns in the text. {1} of those were unisemous and {2} were polysemous. '\
          'The proportion of polysemous nouns is {3:.2f}.\n'.format(noun_count, us_words, ps_words, ps_words/noun_count))
    if ps_words == 1:
        print('2.\nThis page contains a polysemous word.\n')
    elif ps_words == 0:
        print('2.\nThis page does not contain any polysemous words.\n')
    elif ps_words > 1:
        print('2.\nThis page contains multiple polysemous words.\n')
    print('3.\nThe average number of senses per polysemous words is {0:.2f}.\n'.format(total_ps_senses/ps_words))
    print('4.\nCount for different number of senses (format: nr of senses:count):\n')
    print(Counter(sense_list))    
    print('\n5.')
    for noun in first_nouns:
        print(noun[0], " : ", lesk(noun[1], noun[0]).definition())
    print("\nIn this case it get about 2/3 words right. Especially words that are very context specific like chain and David"\
    " seem to be difficult, however it does get some tricky cases right like the word chicken. In this case it was"\
    " indeed meant as the food chicken and not the animal itself.\n")
    print("6.\nNo, this did not happen. Yes it can, depending on the sentence that belongs to the word. If the word around the main word"\
          " differs too much in context, the wrong definition will be found.\n")
    print("7.\nI did expect that some words would be correct, when they were not. For instance 'David' is placed in the correct context"\
          " and was still given a wrong definition.\n")
    print("8.\nDisambiguation can help assign the right meaning of a word to that word. This can help link to the right Wikipedia"\
    " page so that for example the sentence \"I am going to school\" will link to the institute and not to the page related to fish.")


if __name__ == '__main__':
    main()
