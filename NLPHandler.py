import queue
import yake
import spacy
from threading import Thread
import time
import WikiHandler
import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal


class AThread(QThread):
    add_source = pyqtSignal()

    def __init__(self, wiki_queue, metrics_queue_1, metrics_queue_2):
        super().__init__()

        # spacy.cli.download("en_core_web_sm")
        self.wikiGUIQueue = wiki_queue
        self.metrics_queue_1 = metrics_queue_1
        self.metrics_queue_2 = metrics_queue_2

    def run(self):
        NLP_handler(self.wikiGUIQueue, self.add_source, self.metrics_queue_1, self.metrics_queue_2)


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

def NLP_handler(wikiGUIQueue, signal_source, metrics_queue_1, metrics_queue_2):
    audioSampleQueue = queue.Queue()
    textSampleQueue = queue.Queue()
    wikiSearchQueue = queue.Queue()
    usedWords = []
    usedKeys = []

    micSampleLength = 10
    nlp = spacy.load("en_core_web_sm")
    thread = Thread(target=sample_from_mic, args=(micSampleLength, audioSampleQueue, textSampleQueue))
    thread.start()
    totalWords = 0
    totalProperNouns = 0
    custom_kw_extractor = yake.KeywordExtractor()

    while 1:
        while textSampleQueue.empty():
            time.sleep(0.1)
        text = textSampleQueue.get()

        doc = nlp(text)
        totalWords += len(doc)
        keywords = custom_kw_extractor.extract_keywords(text)
        sorted(keywords, key=lambda x: x[1], reverse=True)
        for index in range(len(keywords)):
            if index > 3:
                break
            metrics_queue_2.put(keywords[index][0])
        for k in keywords:
            if k[0] not in usedKeys:
                usedKeys.append(k[0])
        extracted_proper_nouns = extract_proper_nouns(doc, usedWords)
        totalProperNouns += len(extracted_proper_nouns)
        metrics1 = [totalWords, totalProperNouns]
        metrics_queue_1.put(metrics1)

        for noun in extracted_proper_nouns:
            wikiSearchQueue.put(noun.text)

        wikiThread = Thread(target=WikiHandler.get_first_wiki, args=(wikiSearchQueue, wikiGUIQueue, usedKeys, signal_source))
        wikiThread.start()


