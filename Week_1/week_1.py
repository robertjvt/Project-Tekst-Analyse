#!/usr/bin/python3

import nltk
from collections import Counter


def longest_sentence(sentences):
    '''
    Returns the first longest sentence found in the input list.
    Will not return others of the same length.
    '''
    return max(sentences, key=len)


def shortest_sentence(sentences):
    '''
    Returns the first shortest sentence found in the input list.
    Will not return others of the same length.
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
        total_sentences += value
        total_length += key * value
    return total_length / total_sentences


def token_types(data):
    '''
    Returns the amount of token types and an alphabetically
    ordered list of token types of a document.
    '''
    word_list = nltk.word_tokenize(data)
    fdist = nltk.FreqDist(word_list)
    alpha_list = []
    for b,f in fdist.items():
        alpha_list.append(b)
    alpha_list = sorted(alpha_list)
    return len(alpha_list), alpha_list


def character_types(data):
    '''
    Returns the amount of character types and an alphabetically
    ordered list of character types of a document.
    '''
    word_list = nltk.word_tokenize(data)
    unique_chars = []
    for word in word_list:
        for char in word:
            if char not in unique_chars:
                unique_chars.append(char)
    unique_chars = sorted(unique_chars)
    return len(unique_chars), unique_chars


def first_20(count_list):
    '''
    This function is used to print each item from a list containing tuples.
    It can be called in the functions top20_character_types(data) and 
    top20_token_types(data).
    '''
    for item in count_list:
        print(item[0], item[1])


def top20_character_types(data):
    '''
    This function returns a three lists containing tuples
    (format: (n-gram), count). The lists are unigrams, bigrams and trigrams
    respectively at character level.
    '''
    unigram_count = Counter(data).most_common(20)
    bigram_count = Counter(list(nltk.bigrams(data))).most_common(20)
    trigram_count = Counter(list(nltk.trigrams(data))).most_common(20)
    return unigram_count, bigram_count, trigram_count


def top20_token_types(data):
    '''
    This function returns a three lists containing tuples
    (format: (n-gram), count). The lists are unigrams, bigrams and trigrams
    respectively at token level.
    '''
    tokens = nltk.word_tokenize(data)
    unigram_count = Counter(tokens).most_common(20)
    bigram_count = Counter(list(nltk.bigrams(tokens))).most_common(20)
    trigram_count = Counter(list(nltk.trigrams(tokens))).most_common(20)
    return unigram_count, bigram_count, trigram_count


def main():
    with open('holmes.txt') as file:
        data = file.read()
    sentences = nltk.sent_tokenize(data)
    longest = longest_sentence(sentences)
    shortest = shortest_sentence(sentences)
    distribution = sentence_distribution(sentences)
    average_length = average_sentence_length(distribution)
    token_type = token_types(data)
    char_types = character_types(data)
    char_unigrams, char_bigrams, char_trigrams = top20_character_types(data)
    token_unigrams, token_bigrams, token_trigrams = top20_token_types(data)
    

if __name__ == "__main__":
    main()
