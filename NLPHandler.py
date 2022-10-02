import queue
import yake
import spacy
from threading import Thread
import time
import WikiHandler
import speech_recognition as sr

#spacy.cli.download("en_core_web_sm")

def sample_from_mic(micSampleLength, audioSampleQueue, textSampleQueue):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            # read the audio data from the default microphone
            print("START TALKING")
            audio_data = r.record(source, duration=micSampleLength)
            thread = Thread(target=audio_to_text, args=(r, audio_data, textSampleQueue))
            thread.start()


def audio_to_text(r, audio_data, textSampleQueue):
    # convert speech to text
    print("Recognizing...")
    try:
        textFromSpeech = r.recognize_google(audio_data)
        textSampleQueue.put(textFromSpeech)
    except sr.UnknownValueError:
        print("Got nothing for you chief")


def extract_proper_nouns(doc, usedWords):
    pos = [tok.i for tok in doc if tok.pos_ == "PROPN"]
    consecutives = []
    current = []
    for elt in pos:
        if len(current) == 0:
            current.append(elt)
        else:
            if current[-1] == elt - 1:
                current.append(elt)
            else:
                if (' '.join([i.text for i in doc[current[0]:current[-1]+1]])) not in usedWords:
                    consecutives.append(current)
                    usedWords.append(' '.join([i.text for i in doc[current[0]:current[-1]+1]]))
                current = [elt]
    if len(current) != 0:
        if (' '.join([i.text for i in doc[current[0]:current[-1] + 1]])) not in usedWords:
            consecutives.append(current)
            usedWords.append(' '.join([i.text for i in doc[current[0]:current[-1] + 1]]))
    return [doc[consecutive[0]:consecutive[-1] + 1] for consecutive in consecutives]

def NLP_handler(window, wikiGUIQueue):
    audioSampleQueue = queue.Queue()
    textSampleQueue = queue.Queue()
    wikiSearchQueue = queue.Queue()
    usedWords = []
    usedKeys = []

    micSampleLength = 10
    nlp = spacy.load("en_core_web_sm")
    thread = Thread(target=sample_from_mic, args=(micSampleLength, audioSampleQueue, textSampleQueue))
    thread.start()

    custom_kw_extractor = yake.KeywordExtractor()

    while 1:
        while textSampleQueue.empty():
            time.sleep(0.1)
        text = textSampleQueue.get()

        doc = nlp(text)
        keywords = custom_kw_extractor.extract_keywords(text)
        for k in keywords:
            if k[0] not in usedKeys:
                usedKeys.append(k[0])
        extracted_proper_nouns = extract_proper_nouns(doc, usedWords)
        for noun in extracted_proper_nouns:
            wikiSearchQueue.put(noun.text)

        WikiHandler.get_first_wiki(wikiSearchQueue, wikiGUIQueue, usedKeys, window)


