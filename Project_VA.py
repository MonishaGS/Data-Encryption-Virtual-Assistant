##############################################################################

# IMPORTING REQUIRED MODULES # 

from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
import pyttsx3
from googletrans import Translator
import webbrowser
import wikipedia
from gtts import gTTS
from playsound import playsound
import os
import subprocess
from PIL import Image
from pytesseract import pytesseract
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

##############################################################################

# LOADING AND INITIALIZING PRE-REQUISITES #

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

va_Laura = pyttsx3.init()
va_Laura.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
va_Laura.setProperty('rate',180)

recog = Recognizer()
mic = Microphone()

translate_client = Translator()
languages = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese', 'zh-tw': 'chinese traditional', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'}
translate_error_message = 'Sorry, Not able to translate. Try Again.'
translate = {}

path_to_tesseract = r"C:/Users/ABI/Desktop/BE CSE/Sem 2 Project/Tesseract/tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('AI_chatbot_model.h5')

##############################################################################

# TEXT TO SPEECH #

def speak_text_cmd(cmd):
    va_Laura.say(cmd)
    va_Laura.runAndWait()

##############################################################################

# OTHER LANGUAGE TEXT TO SPEECH #

def g_speak(text, language = 'en'):
    try:
        voice = gTTS(text = text, lang = language)
        voice.save("voice.mp3")
        playsound("voice.mp3")
        os.remove("voice.mp3")
    except ValueError:
        pass

##############################################################################

# TEXT THROUGH SPEECH RECOGNITION #

def listen(lang = 'en-US'):
    recognized = ""
    while recognized == "":
        with mic:
            audio = recog.listen(mic,3, 5)
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

##############################################################################

# TRANSLATOR #

def translate():
    print("\nFrom what language ? ", end = '')
    src = listen()
    print("\nTo what language ? ", end = '')
    dest = listen()

    src_code = ''
    dest_code = ''

    for i in languages:
        if languages[i] == src:
            src_code = i
        elif languages[i] == dest:
            dest_code = i
        if dest_code != '' and src_code != '':
            break

    if src_code == '':
        print("Source language not found. Please try again\n")
        return None
    if dest_code == '':
        print("Destination language not found. Please try again\n")
        return None

    print("\nPhrase : ", end = '')
    phrase = listen(src_code)
    try:
        translate = translate_client.translate(phrase, dest = dest_code, src = src_code)
        print("\nTranslated text :", translate.text)
        g_speak(translate.text, dest_code)
    except AttributeError:
        print(translate_error_message)
    except  IndexError:
        print(translate_error_message)

##############################################################################

# OPEN APPLICATION #

def open_application(cmd):
    if cmd == "e":
        subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
    elif cmd == "b":
        subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
    elif cmd == "c":
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
    elif cmd == "d":
        os.system("notepad")
    '''elif "media player" in cmd:
        print("Opening media player")
        speak_text_cmd("Opening media player")
        os.startfile("C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe")
    elif "ccleaner" in cmd:
        print("Opening ccleaner")
        speak_text_cmd("Opening ccleaner")
        os.startfile("C:\Program Files\CCleaner\CCleaner64.exe")'''

##############################################################################

# OCR #

def image_to_text():
    speak_text_cmd("Enter image path with extension")
    image_path = input("Enter image path with extension :")
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        print(text[:-1])
    except FileNotFoundError:
        print("Fie not found. Try again")

##############################################################################

# INTERNET SEARCH #

def internet_search(cmd):
    if cmd == "i":
        results = ""
        while results == "":
            print("What do you want to search?")
            cmd = listen()
            try:
                results = wikipedia.summary(cmd, sentences = 3)
            except wikipedia.exceptions.DisambiguationError:
                print("Please give a specific search")
                continue
            except wikipedia.exceptions.PageError:
                print("Page doesn't exist. Try again")
                continue
            speak_text_cmd("According to Wikipedia")
            print(results)
            speak_text_cmd(results)

    elif cmd == "g":
        webbrowser.get("google-chrome").open("youtube.com")

    elif cmd == "f":
        webbrowser.get("google-chrome").open('https://www.google.co.in/')

    elif cmd == "h":
        webbrowser.get("google-chrome").open("stackoverflow.com")

##############################################################################

# CHOOSE ONE OF THE ABOVE FUNCTIONS ACCORDING TO INPUT #

def reply(task):
    if ((task>="a") and (task<="l")):
        if task == "a":
            translate()
        elif ((task>="b") and (task<="e")):
            open_application(task)
        elif ((task>="f") and (task<="i")):
            internet_search(task)
        elif task == "k":
            image_to_text()
    else:
        pass
    print("\n")

##############################################################################

# PRE-PROCESSING TEXT AND CATEGORIZING IT #

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
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result, tag

##############################################################################

# MAIN FUNCTION #

print("BOT IS READY!")
speak_text_cmd("BOT IS READY!")

while True:
    print("You : ")
    message = listen()
    ints = predict_class(message)
    if ints == []:
        print("Sorry I don't understand your statement. Can you please repeat?")
        speak_text_cmd("Sorry I don't understand your statement. Can you please repeat?")
    else:
        res, tag = get_response(ints, intents)
        print("Bot : ", res)
        speak_text_cmd(res)
        if tag == "goodbye":
            exit()
        reply(tag)

##############################################################################