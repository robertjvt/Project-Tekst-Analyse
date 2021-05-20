import wikipedia
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag


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


def main():
    wiki = wikipedia.page('Colonel Sanders')
    content = wiki.content
    noun_list = noun_finder(content)
    print(noun_list)


if __name__ == '__main__':
    main()
