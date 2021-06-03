import sys
import os
import wikipedia


def wiki_finder(NE):
    wiki_search = wikipedia.search(NE)
    try:
        page = wikipedia.page(wiki_search[0])
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[0])

    return page.url


def main():
    NE_list = ['Obama', 'Facebook', 'Mexico', 'USA', 'KFC']
    for NE in NE_list:
        url = wiki_finder(NE)
        print(url)


if __name__ == '__main__':
    main()
