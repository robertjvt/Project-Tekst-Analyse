from nltk.tag import StanfordNERTagger
import nltk
import requests
import json
from nltk.parse import CoreNLPParser
from nltk.corpus import wordnet
import exercise_1


def alternative_stanford_ner():
    '''
    Conducts NER based on StanfordNLP NER.
    Allows for looping through the entire JSON that is returned.
    '''
    ner = requests.post('http://[::]:9000/?properties={"annotators":"ner","outputFormat":"json"}', data = {'data':data}).text

    y = json.loads(ner)
    x = y['sentences']
    for sentence in x:
        for word in sentence['tokens']:
            if word.get('ner') != 'O':
                print(word.get('word') + "\t" + word.get('ner'))
        print("\n")


def stanford_ner(data):
    '''
    Conducts NER based on StanfordNLP NER.
    Only offers a simple list with the data and the recognized entity.
    '''
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    return list(ner_tagger.tag((data.split())))


def wordnet_ner(lem_nouns):
    '''
    Conducts NER based on WordNet.
    Bases its recognized entities on the similarity of the words and the defined entities.
    '''
    entities = ['location', 'person', 'organization']
    recognized_entities = []
    for word in lem_nouns:
        highest_similarity = 0
        matched_entity = ''
        for entity in entities:
            similarity = exercise_1.similarity(exercise_1.noun_synset([word]), exercise_1.noun_synset([entity]))
            if similarity != [] and similarity[0] >= highest_similarity:
                highest_similarity = similarity[0]
                matched_entity = entity
        recognized_entities.append((word, matched_entity))
    return recognized_entities


def main():
    with open('ada_lovelace.txt', 'r') as file:
        data = file.read()
    stanford_entities = stanford_ner(data) 
    tokens = nltk.word_tokenize(data)
    pos_tagged_list = exercise_1.pos_tags(tokens)
    noun_list = exercise_1.nouns_pos_tags(pos_tagged_list)
    lem_nouns = exercise_1.noun_lemmatize(noun_list)       
    wordnet_entities = wordnet_ner(lem_nouns)


if __name__ == "__main__":
    main()

