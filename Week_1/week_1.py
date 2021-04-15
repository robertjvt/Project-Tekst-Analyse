#!/usr/bin/python3

import nltk


def longest_sentences(sentences):
    # Kan op deze manier of op de simpelere manier hieronder (die returned echter maar 1).
    '''
    Returns the longest sentences found in the input list.
    '''
    longest_sentence = ''
    longest_sentences = []
    
    for sentence in sentences:
        if len(sentence) > len(longest_sentence):
            longest_sentence = sentence
            if longest_sentences != []:
                longest_sentences.clear()
                longest_sentences.append(sentence)
            else:
                longest_sentences.append(sentence)
        elif len(sentence) == len(longest_sentence):
            longest_sentences.append(sentence)
        
    return longest_sentences


def longest_sentence(sentences):
    '''
    Returns the first longest sentence found in the input list.
    '''
    return max(sentences, key=len)


def shortest_sentence(sentences):
    '''
    Returns the first shortest sentence found in the input list.
    '''
    return min(sentences, key=len)


def sentence_distribution(sentences):
    '''
    Returns the distribution of sentence length.
    '''
    distribution = {}
    for sentence in sentences:
        length = len(sentence)
        distribution[length] = distribution.get(length, 0) + 1
    return distribution


def average_sentence_length(distribution):
    '''
    Calculates the average sentence length of a document.
    '''
    total_sentences = 0
    total_length = 0
    for key, value in distribution.items():
        total_sentences += key
        total_length += value
    return total_sentences / total_length

    
def main():
    with open('holmes.txt') as file:
        data = file.read()

    sentences = nltk.sent_tokenize(data)
    longest = longest_sentences(sentences)
    shortest = shortest_sentence(sentences)
    distribution = sentence_distribution(sentences)
    average_length = average_sentence_length(distribution)
    
if __name__ == "__main__":
    main()
