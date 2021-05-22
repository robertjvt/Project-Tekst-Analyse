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


def print_1to8(noun_count, us_words, ps_words, total_ps_senses, sense_list):
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
    print_1to8(noun_count, us_words, ps_words, total_ps_senses, sense_list)
    return synset_list, nouns_list


def main():
    wiki = wikipedia.page('Colonel Sanders')
    content = wiki.content
    noun_list = noun_finder(content)
    synset_list, first_nouns = synsets(noun_list)
    
    print('5.')
    for noun in first_nouns:
        print(noun[0], " : ", lesk(noun[1], noun[0]).definition())
    print("\nIn this case it get about 2/3 words right. Especially words that are very context specific like chain and David"\
    "seem to be difficult, however it does get some tricky cases right like the word chicken. In this case it was"\
    "sindeed meant as the food chicken and not the animal itself.")
    print('6.')
    
    print('7.')
    print("""  """)
    
    print('8.')
    print("Disambiguation can help assign the right meaning of a word to that word. This can help link to the right Wikipedia"\
    "page so that for example the sentence \"I am going to school\" will link to the institute and not to the page related to fish.")

if __name__ == '__main__':
    main()
