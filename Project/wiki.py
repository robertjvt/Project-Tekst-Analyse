from mediawiki import MediaWiki


def wiki_finder(NE):
    wikipedia = MediaWiki()
    wiki_search = wikipedia.search(NE)
    page = wikipedia.page(wiki_search[0])
    return page.url


def main():
    NE_list = ['Obama', 'Facebook', 'Mexico', 'USA', 'KFC']
    for NE in NE_list:
        url = wiki_finder(NE)
        print(url)


if __name__ == '__main__':
    main()
