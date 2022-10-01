# defines a set of functions for calling the wiki api
import wikipedia
import random
from bing_image_urls import bing_image_urls


def get_first_wiki(term, language="en"):
    if language in wikipedia.languages():
        wikipedia.set_lang(language)
    else:
        # set failure condition
        wikipedia.set_lang("en")

    # gets the article titles related to term
    article_list = wikipedia.search(term)

    print(article_list)

    # if the list is empty, might be misspelled
    if len(article_list) == 0:
        article_list = wikipedia.suggest(term)

    wiki_page = search_title_random(article_list[0])
    page_image = bing_image_urls(wiki_page.title, limit=1)[0]

    return wiki_page, page_image


def search_title_random(title):
    try:
        # There might be many things named this still
        wiki_page = wikipedia.page(title)
    except wikipedia.DisambiguationError as e:
        # This is not great, could be a better suggestion mechanism
        print("choosing random article")
        s = random.choice(e.options)

        wiki_page = search_title_random(s)

    return wiki_page