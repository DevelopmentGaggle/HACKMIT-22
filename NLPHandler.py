import queue
import yake
import spacy
from threading import Thread
import time
import speech_recognition as sr

#spacy.cli.download("en_core_web_sm")

def sample_from_mic(micSampleLength, audioSampleQueue, textSampleQueue):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            # read the audio data from the default microphone
            print("START TALKING")
            audio_data = r.record(source, duration=micSampleLength)
            audioSampleQueue.put(audio_data)
            thread = Thread(target=audio_to_text, args=(r, audioSampleQueue, textSampleQueue))
            thread.start()


def audio_to_text(r, audioSampleQueue, textSampleQueue):
    # convert speech to text
    print("Recognizing...")
    audio_data = audioSampleQueue.get()
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


audioSampleQueue = queue.Queue()
textSampleQueue = queue.Queue()
usedWords = []
usedKeys = []


micSampleLength = 10
nlp = spacy.load("en_core_web_sm")
thread = Thread(target=sample_from_mic, args=(micSampleLength, audioSampleQueue, textSampleQueue))
thread.start()

custom_kw_extractor = yake.KeywordExtractor()

while 1:
    while textSampleQueue.empty():
        time.sleep(0.5)
    text = textSampleQueue.get()
    """The Monroe Doctrine was a United States foreign policy position that opposed European colonialism
    in the Western Hemisphere. It held that any intervention in the political affairs of the Americas by foreign
    powers was a potentially hostile act against the United States. The doctrine was central to American foreign
    policy for much of the 19th and early 20th centuries. President James Monroe first articulated
    the doctrine on December 2, 1823, during his seventh annual State of the Union Address to Congress (though
    it would not be named after him until 1850). At the time, nearly all Spanish colonies in the Americas had either achieved
    or were close to independence. Monroe asserted that the New World and the Old World were to remain distinctly separate spheres of
    influence, and thus further efforts by European powers to control or influence sovereign states in the region would be
    viewed as a threat to U.S. security. In turn, the United States would recognize and not interfere with existing European colonies
    nor meddle in the internal affairs of European countries."""

    doc = nlp(text)
    keywords = custom_kw_extractor.extract_keywords(text)
    for k in keywords:
        if k[0] not in usedKeys:
            usedKeys.append(k[0])
    print(usedKeys)

    extractedProperNouns = extract_proper_nouns(doc, usedWords)
    #print(extractedProperNouns)

