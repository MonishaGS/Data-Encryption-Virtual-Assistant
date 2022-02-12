import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

##################

from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
import pyttsx3
va_Laura = pyttsx3.init()
va_Laura.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
va_Laura.setProperty('rate',200)

recog = Recognizer()
mic = Microphone()

##################

def speak_text_cmd(cmd):
    va_Laura.say(cmd)
    va_Laura.runAndWait()

def listen():
    recognized = ""
    while recognized == "":
        with mic:
            audio = recog.listen(mic, 5, 5)
        try:
            recognized = recog.recognize_google(audio)
        except UnknownValueError:
            pass
        except TimeoutError:
            pass
        except RequestError:
            print("Sorry network error. Please try again")
        rcgnd = recognized.lower()
    print(rcgnd)
    return rcgnd

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('AI_chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x : x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({'intent' : classes[r[0]], 'probability' : str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    print(intents_list)
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("BOT IS READY. SUIT UP!")

while True:
    print("You :", end = ' ')
    message = listen()
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("Bot : ", res)
    speak_text_cmd(res)    