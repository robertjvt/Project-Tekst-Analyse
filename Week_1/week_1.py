#!/usr/bin/python3

import nltk


def longest_sentence(sentences):
    longest_sentence = ''
    longest_sentences = []
    
    for sentence in sentences:
        if len(sentence) > len(longest_sentence):
            longest_sentence = sentence
            if longest_sentences != []:
                longest_sentences.pop()
            longest_sentences.append(sentence)
        elif len(sentence) == len(longest_sentence):
            longest_sentence.append(sentence)
        
    return(longest_sentences)
    

def main():
    with open('holmes.txt') as file:
        data = file.read()

    sentences = nltk.sent_tokenize(data)

if __name__ == "__main__":
    main()
