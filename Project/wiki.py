import sys
import os
import wikipedia as wiki


def wiki_finder(NE):
    wiki_search = wiki.search(NE)
    page = wiki.page(wiki_search[0], auto_suggest = True)
    
    return page.url



def main():
    NE_list = ['Obama', 'Facebook', 'Mexico']
    for NE in NE_list:
        url = wiki_finder(NE)

if __name__ == '__main__':
    main()
