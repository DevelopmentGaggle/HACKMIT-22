# defines a set of functions for calling the wiki api
import wikipedia
import random
import yake
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

    wiki_page = find_best_match(article_list[0])
    page_image = bing_image_urls(wiki_page.title, limit=1)[0]

    return wiki_page, page_image


def find_best_match(title):
    try:
        # There might be many things named this still
        wiki_page = wikipedia.page(title)
    except wikipedia.DisambiguationError as e:
        # This is not great, could be a better suggestion mechanism
        print("Disambiguation! Attempting to find most relevant article...")
        custom_kw_extractor = yake.KeywordExtractor()
        counts = []
        for o in e.options:
            keywords = custom_kw_extractor.extract_keywords(wikipedia.page(title).summary)
            articleKeys = []
            for k in keywords:
                if k[0] not in articleKeys:
                    articleKeys.append(k[0])
                cnt = 0
            for phrase in XXX:
                if phrase in articleKeys:
                    cnt = cnt + 1
            counts.append(cnt)
            max = counts[0]
            opt = 0
        for num in range(1, len(counts)):
            if max < counts[num]:
                max = counts[num]
                opt = num

        wiki_page = find_best_match(e.options[opt])
    return wiki_page