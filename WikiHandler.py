# defines a set of functions for calling the wiki api
import wikipedia
import random
import yake
from bing_image_urls import bing_image_urls


def get_first_wiki(wikiSearchQueue, wikiGUIQueue, usedKeys, signal_source, language="en"):
    if language in wikipedia.languages():
        wikipedia.set_lang(language)
    else:
        # set failure condition
        wikipedia.set_lang("en")

    while not wikiSearchQueue.empty():
        term = wikiSearchQueue.get()
        # gets the article titles related to term

        article_list = wikipedia.search(term)
        print(article_list)
        # if the list is empty, might be misspelled.
        if len(article_list) == 0:
            article_list = wikipedia.suggest(term)

        if len(article_list) == 0:
            return

        wiki_page = find_best_match(article_list[0], usedKeys)
        try:
            imageLinks = bing_image_urls(wiki_page.title, limit=1)
        except:
            imageLinks = []

        if len(imageLinks) > 0:
            page_image = imageLinks[0]
        else:
            page_image = ""

        wikiGUIQueue.put([wiki_page, page_image])
        signal_source.emit()

def find_best_match(title, usedKeys):
    try:
        # There might be many things named this still
        print(title)
        wiki_page = wikipedia.page(title, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        # This is not great, could be a better suggestion mechanism
        print("Disambiguation! Attempting to find most relevant article...")
        print(e.options)
        custom_kw_extractor = yake.KeywordExtractor()
        counts = []
        mostRelevant = 5
        for o in e.options:
            if mostRelevant == 0:
                break;
            mostRelevant = mostRelevant - 1
            keywords = custom_kw_extractor.extract_keywords(find_best_match(o, usedKeys).summary)
            articleKeys = []
            for k in keywords:
                if k[0] not in articleKeys:
                    articleKeys.append(k[0])
                cnt = 0
            for phrase in usedKeys:
                if phrase in articleKeys:
                    cnt = cnt + 1
            counts.append(cnt)
        max = counts[0]
        opt = 0
        for num in range(1, len(counts)):
            if max < counts[num]:
                max = counts[num]
                opt = num

        wiki_page = find_best_match(e.options[opt], usedKeys)
    return wiki_page