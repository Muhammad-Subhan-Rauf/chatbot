import random

import json

from jokeapi import Jokes

import pickle

import numpy as np

import nltk
from nltk import WordNetLemmatizer

from gtts import gTTS

import asyncio

import time

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from tensorflow import keras

import keras.models

from keras.models import load_model


from speech_recog import speech_to_text, text_to_speech
import tkinter as tk

window = None

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


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
    err_thresh = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > err_thresh]


    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    try:
        tag = intents_list[0]['intent']

        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    except:
        print("INVALID INPUT ERROR")
        text_to_speech("INVALID INPUT ERROR")
def main():
    text_or_speech = input("Do you prefer i speak(S) or write(W)??: ").lower()
    print("GO! Bot is running")

    ints = predict_class("")

    while True:

        if text_or_speech == "w":
            message = input("")
            ints = predict_class(message)
            res = get_response(ints, intents)


            if ints[0]['intent'] == "addition":
                res=do_addition(res,message)
            if ints[0]['intent'] == "subtraction":
                res=do_subtraction1(res,message)
            
            
            print(res)
            text_to_speech(res)
            continue
        else:
            message = speech_to_text()
            if message==False:
                print("Say something that i can understand you twat")
                text_to_speech("Say something that i can understand you twat")
                continue
            ints = predict_class(message)
            res = get_response(ints, intents)
            
            if ints[0]['intent'] == "joke":
                asyncio.run(print_joke())
            if ints[0]['intent'] == "addition":
                res=do_addition(res,message)
            if ints[0]['intent'] == "subtraction1":
                res=do_subtraction1(res,message)
            if ints[0]['intent'] == "subtraction2":
                res=do_subtraction2(res,message)
            
            
            print(res)
            text_to_speech(res)
    
async def print_joke():
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(blacklist=["nsfw","explicit"],category=["dark"])  # Retrieve a random joke
    
    if joke["type"] == "single": # Print the joke
        text_to_speech (joke["joke"])
    else:
        text_to_speech (joke["setup"])
        time.sleep(0.5)
        text_to_speech (joke["delivery"])
    return joke
        
        
def do_addition(res,message):
    numbers = [int(s) for s in message.split() if s.isdigit()]
    result = res.replace("{number1}",str(numbers[0]))
    result = result.replace("{number2}",str(numbers[1]))
    result = result.replace("{result}",str(numbers[0]+numbers[1]))
    return result

def do_subtraction1(res,message):
    print(message)
    print(res)
    numbers = [int(s) for s in message.split() if s.isdigit()]
    result = res.replace("{number1}",str(numbers[0]))
    result = result.replace("{number2}",str(numbers[1]))
    result = result.replace("{result}",str(numbers[0]-numbers[1]))
    return result

def do_subtraction2(res,message):
    numbers = [int(s) for s in message.split() if s.isdigit()]
    result = res.replace("{number2}",str(numbers[1]))
    result = result.replace("{number1}",str(numbers[0]))
    result = result.replace("{result}",str(numbers[1]-numbers[0]))
    return result






def button1_command():
    
    new_window = tk.Toplevel(window)
    new_window.title("Response Window")

    text_box = tk.Entry(new_window)
    text_box.pack(pady=10)

    
   
    
    
    def store_text_command():
        message = text_box.get()
        
        
        ints = predict_class(message)
        res = get_response(ints, intents)

        
        
        response_text.config(state=tk.NORMAL)  # Enable editing
        response_text.delete(1.0, tk.END)      # Clear previous content
        response_text.insert(tk.END, f"Your input:  {message}")  # Add new content
        response_text.config(state=tk.DISABLED)
        
        
        if ints[0]['intent'] == "addition":
            res=do_addition(res,message)
        if ints[0]['intent'] == "subtraction1":
            res=do_subtraction1(res,message)
        if ints[0]['intent'] == "subtraction2":
            res=do_subtraction2(res,message)
        
        
        print(res)
        text_to_speech(res)
        
        
        j=None
        response_text.config(state=tk.NORMAL)  # Enable editing

        if ints[0]['intent'] == "joke":
            j = asyncio.run(print_joke())
            if j["type"] == "single": # Print the joke
                print(j["joke"])
                response_text.insert(tk.END, "\n" + ((res + j["joke"]) if j!=None else (res)))  # Add new content
            else:
                print(j["setup"])
                response_text.insert(tk.END, "\n" + ((res + j["setup"]) if j!=None else (res)))  # Add new content
                print(j["delivery"])
                response_text.insert(tk.END, "\n" + ((res + j["delivery"]) if j!=None else (res)))  # Add new content
        else:
            response_text.insert(tk.END, "\n" + ((res) if j!=None else (res)))  # Add new content
            
        response_text.config(state=tk.DISABLED)
        
        
        
    store_button = tk.Button(new_window, text="Enter", command=store_text_command)
    store_button.pack(pady=10)

    
    
    response_text = tk.Text(new_window, height=5, width=30, state=tk.DISABLED)
    response_text.pack(pady=10)

def button2_command():
    new_window = tk.Toplevel(window)
    new_window.title("Response Window")

    
    
    

    def store_speak_command():
        text_to_speech("You may speak now")
        spoken = speech_to_text()
        user_label.config(text=f"You entered: {spoken}")
        
        response_text.config(state=tk.NORMAL)  # Enable editing
        response_text.delete(1.0, tk.END)      # Clear previous content
        response_text.insert(tk.END, f"Your input:  {spoken}")  # Add new content
        response_text.config(state=tk.DISABLED)
        
        if not spoken:
            
            
            return False
        ints = predict_class(spoken)
        res = get_response(ints, intents)
        
        
        if ints[0]['intent'] == "addition":
            res=do_addition(res,spoken)
        if ints[0]['intent'] == "subtraction1":
            res=do_subtraction1(res,spoken)
        if ints[0]['intent'] == "subtraction2":
            res=do_subtraction2(res,spoken)
        
        
        print(res)
        text_to_speech(res)
        result_label.config(text=res)
        
        j=None
        response_text.config(state=tk.NORMAL)  # Enable editing

        if ints[0]['intent'] == "joke":
            j = asyncio.run(print_joke())
            if j["type"] == "single": # Print the joke
                print(j["joke"])
                response_text.insert(tk.END, "\n" + ((res + j["joke"]) if j!=None else (res)))  # Add new content
            else:
                print(j["setup"])
                response_text.insert(tk.END, "\n" + ((res + j["setup"]) if j!=None else (res)))  # Add new content
                print(j["delivery"])
                response_text.insert(tk.END, "\n" + ((res + j["delivery"]) if j!=None else (res)))  # Add new content
        else:
            response_text.insert(tk.END, "\n" + ((res) if j!=None else (res)))  # Add new content
            
        response_text.config(state=tk.DISABLED)
        
        
        
    store_button = tk.Button(new_window, text="speak", command=store_speak_command)
    store_button.pack(pady=10)

    user_label = tk.Label(new_window, text="")
    user_label.pack(pady=10)
    
    result_label = tk.Label(new_window, text="Waiting for you")
    result_label.pack(pady=10)

    response_text = tk.Text(new_window, height=5, width=30, state=tk.DISABLED)
    response_text.pack(pady=10)



# Create the main window
window = tk.Tk()
window.title("CHATBOT")

# Create buttons
button1 = tk.Button(window, text="Writing Bot", command=button1_command)
button2 = tk.Button(window, text="Speaking Bot", command=button2_command)

# Create a label to display the result
label = tk.Label(window, text="Click a button")



# Pack the widgets into the window
button1.pack(pady=10)
button2.pack(pady=10)
label.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()