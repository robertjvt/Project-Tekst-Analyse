# Exercise 1, assignment week 3
# Names: Robert van Timmeren, Kylian de rooij, Remi Thüss

import nltk
import re
from operator import itemgetter
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def pos_tags(tokens):
    '''
    Returns a list of POS-tagged tokens from a list of tokens
    '''
    return nltk.pos_tag(tokens)


def nouns_pos_tags(tagged_list):
    '''
    Returns a list of all nouns from a list of POS-tagged tokens
    '''
    noun_list = []
    for item in tagged_list:
        if item[1] == 'NN' or item[1] == 'NNP' or item[1] == 'NNS':
            noun_list.append(item[0])
    return noun_list

    
def noun_lemmatize(noun_list):
    '''
    returns a list of lemmatized nouns from a list of nouns
    '''
    lem_nouns = []
    synset = ''
    for item in noun_list:
        lem_nouns.append(lemmatizer.lemmatize(item, wordnet.NOUN))
    return lem_nouns


def noun_synset(lem_nouns):
    '''
    returns a list of synsets of lemmatized nouns
    '''
    noun_synset = []
    for item in lem_nouns:
        if len(wordnet.synsets(item, pos='n')) > 0:
            noun_synset.append(wordnet.synsets(item, pos='n'))
    return noun_synset


def hypernymOf(synset1, synset2):
    ''' 
    Returns True if synset2 is a hypernym of
    synset1, or if they are the same synset.
    Returns False otherwise. 
    '''
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if hypernymOf(hypernym, synset2):
            return True
    return False


def hypernym_comparison(noun_synsets, words_compare):
    '''
    Compares a list of synsets to another lists of synsets to look
    for references and prints the words and the references.
    '''
    for synset in noun_synsets:
        if isinstance(synset, list):
            synset = synset[0]
        for word in words_compare:
            if isinstance(word, list):
                word = word[0]
            if hypernymOf(word, synset) == True:
                word = re.sub(r'(Synset\()\'(.*?)(.n.01)\'(\))', r'\2' ,str(word))
                reference = re.sub(r'(Synset\()\'(.*?)(.n.01)\'(\))', r'\2' ,str(synset))
                print('{0} --> {1}'.format(word, reference))


def alt_noun_class(synset, top_classes):
    alt_noun_class = ''
    x = 0
    while x != 1:
        if len(synset.hypernyms()) > 0:
            if str(synset.hypernyms()[0])[8:-7] in top_classes:
                alt_noun_class = str(synset.hypernyms()[0])[8:-7]
                break
            else:
                synset = synset.hypernyms()[0]
        else:
            break
    return alt_noun_class


def noun_class(noun_list):
    top_classes = ('act', 'action', 'activity', 'animal', 'fauna', 'artifact',
                   'attribute', 'property', 'body', 'corpus', 'cognition',
                   'knowledge', 'communication', 'event', 'happening',
                   'feeling', 'emotion', 'food', 'group', 'collection',
                   'location', 'place', 'motive', 'natural_object',
                   'natural_phenomenon', 'person', 'human_being', 'plant',
                   'flora', 'possession', 'process', 'quantity', 'amount',
                   'relation', 'shape', 'state', 'condition', 'substance',
                   'time')
    noun_class_list = []
    total_synsets = 0
    total_nouns = len(noun_list)
    single_ss_nouns = 0
    multiple_ss_nouns = 0
    for noun in noun_list:
        noun_ss = wordnet.synsets(noun, pos='n')
        total_synsets += len(noun_ss)
        if len(noun_ss) == 1:
            single_ss_nouns += 1
        elif len(noun_ss) > 1:
            multiple_ss_nouns += 1
        for synsets in noun_ss:
            if len(synsets.hypernyms()) > 0:
                if str(synsets.hypernyms()[0])[8:-7] in top_classes:
                    noun_class_list.append(str(synsets.hypernyms()[0])[8:-7])
                else:
                    noun_class = alt_noun_class(synsets.hypernyms()[0],
                                                top_classes)
                    noun_class_list.append(noun_class)
    return noun_class_list, single_ss_nouns, total_synsets/total_nouns, multiple_ss_nouns


def similarity(syn_list_1, syn_list_2):
    '''
    For 2 lists of synsets of words returns a list of their similarity
    '''
    i = -1
    sim = []
    for syn in syn_list_1:
        i += 1
        if isinstance(syn, list):
            syn = syn[0]
        if isinstance(syn_list_2[i], list):
            syn_list_2[i] = syn_list_2[i][0]
            sim.append(syn.wup_similarity(syn_list_2[i]))
    return sim


def sort_list(li1, li2, li3):
    '''
    Combines 3 lists into tuples into a new and sorted lists
    where li1[0], li2[0], li3[0] are: [(li1[0], li2[0], li3[0])]
    '''
    i = -1
    wordlist = []
    for item in li1:
        i += 1
        tuples = (item, li2[i], li3[i])
        wordlist.append(tuples)
    wordlist.sort(key=itemgetter(2), reverse=True)
    return wordlist


def main():
    text = open('ada_lovelace.txt').read()
    tokens = nltk.word_tokenize(text)
    pos_tagged_list = pos_tags(tokens)
    noun_list = nouns_pos_tags(pos_tagged_list)
    lem_nouns = noun_lemmatize(noun_list)
    noun_synsets = noun_synset(lem_nouns)

    words_compare = [wordnet.synsets('relative', pos='n'), wordnet.synsets('science', pos='n'), 
                     wordnet.synsets('illness', pos='n')]
    
    print('1a ,b ,c:')
    hypernym_comparison(noun_synsets, words_compare)
    print('So there is 1 reference to \'relative\', 2 references to \'science\' and no references to \'illness\'\n')
    
    print('2:')
    noun_class_list, single_ss_nouns, avg_ss, multiple_ss_nouns = noun_class(noun_list)
    print('First 20 nouns by top 25 noun classes:', '\n',\
          noun_class_list[0:20], '\n')
    print('Amount of Nouns with a single hypernym:',\
          single_ss_nouns)
    print('Examples:')
    print('Word: \'insanity\' Hypernym: Synset(\'insanity.n.01\')')
    print('Word: \'programmer\' Hypernym: Synset(\'programmer.n.01\')')
    print('Word: \'mathematics\' Hypernym: Synset(\'mathematics.n.01\')\n')
    print('Amount of times system had to choose between multiple hypernyms:',\
          multiple_ss_nouns)
    print('Examples:')
    print('Word: \'engine\' Hypernyms: [Synset(\'engine.n.01\'), Synset(\'engine.n.02\'), Synset(\'locomotive.n.01\'), Synset(\'engine.n.04\')]')
    print('Word: \'computer\' Hypernyms: [Synset(\'computer.n.01\'), Synset(\'calculator.n.01\')]')
    print('Word: \'mother\' Hypernyms: [Synset(\'mother.n.01\'), Synset(\'mother.n.02\'), Synset(\'mother.n.03\'), Synset(\'mother.n.04\'), Synset(\'mother.n.05\')]\n'
)
    print('Average hypernyms per noun: {:.2f}\n'.format(avg_ss))
    
    print('3:')
    words_1 = ['car', 'coast', 'food', 'journey', 'monk', 'moon']
    words_2 = ['automobile', 'shore', 'fruit', 'car', 'slave', 'string']
    word_similarity = similarity(noun_synset(words_1), noun_synset(words_2))
    sorted_sim_list = sort_list(words_1, words_2, word_similarity)
    for y in range(5):
        print('{0} - {1} --> {2}'.format(sorted_sim_list[y][0], sorted_sim_list[y][1] , sorted_sim_list[y][2]))
    print('As the actual scores are not relevant, the results from the above similarity are quite similar to '
          'the results of George Miller and Walter Charles with the exception being food - fruit. This is most '
          'likely due to a difference between the hypernym/hyponym structure of wordnet and the way people percieve '
          'the difference between these two words.')


if __name__ == '__main__':
    main()
