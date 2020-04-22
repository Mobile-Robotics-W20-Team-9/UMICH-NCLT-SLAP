# from python example and tutorial here: https://data-flair.training/blogs/python-chatbot-project/

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import spacy
import tkinter
from tkinter import *

from keras.models import load_model
model = load_model('chatbot_model.h5')
modelBuilding = load_model('buildings_model.h5')
import json
import random
intents = json.loads(open('intents/intents.json').read())
words = pickle.load(open('pickles/words.pkl','rb'))
classes = pickle.load(open('pickles/classes.pkl','rb'))
buildingsIntents = json.loads(open('intents/buildingIntents.json').read())
building_words = pickle.load(open('pickles/building_words.pkl','rb'))
buildings = pickle.load(open('pickles/buildings.pkl','rb'))
confirmation = 0
startNav = 0 #TODO: START CONVERSION TO GPS COORDINATES
completedNav = 0 #TODO: Add response once complete
emergencyExit = 0 #TODO: OPTIONAL STOP EVERYTHING

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, wording, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(wording)
    for s in sentence_words:
        for i,word in enumerate(wording):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def predict_building(currbuilding):
    # filter below  threshold predictions
    p = bag_of_words(currbuilding, building_words,show_details=False)
    res = modelBuilding.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"buildingIntents": buildings[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def getBuildingInfo(sentence):
    doc = nlp(sentence)
    start = 0
    end = 0
    startBuilding = "random location"
    stopBuilding = "random location"
    for token in doc:
        if token.pos_ == "PROPN" and start == 1:
            startBuilding = token.text
        elif token.pos_ == "PROPN" and end == 1:
            stopBuilding = token.text
        elif token.text == "to":
            start = 0
            end = 1
        elif token.text == "from":
            start = 1
            end = 0
        else:
            pass
            # print(token.text)
    return [startBuilding, stopBuilding]


#Creating tkinter GUI
def send():
    msgClean = EntryBox.get("1.0",'end-1c')
    msg = msgClean.strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "You: " + msg + '\n\n')
        ChatBox.config(foreground="#446665", font=("Verdana", 12 ))

        ints = predict_class(msg)
        global confirmation
        global startNav
        global emergencyExit
        # adds rule based chatbot to confirm navigation
        if (ints[0]['intent'] == "yes" or ints[0]['intent'] == "no") and confirmation == 1 and startNav == 0:
            emergencyExit = 0
            if ints[0]['intent'] == "yes":
                res = "Starting navigation. Please wait for process to complete. This may take a couple minutes."
                startNav = 1
            elif ints[0]['intent'] == "no":
                res = "Cancelled operation"
            confirmation = 0
        elif ints[0]['intent'] == "navigation" and startNav == 0:
            emergencyExit = 0
            currbuilding = getBuildingInfo(msgClean)
            if currbuilding[0] == 'random location':
                currbuilding[0] = buildings[random.randint(0, len(buildings)-1)] 
                while currbuilding[0] == currbuilding[1]:
                    currbuilding[1] = buildings[random.randint(0, len(buildings)-1)]
            if currbuilding[1] == 'random location':
                currbuilding[1] = buildings[random.randint(0, len(buildings)-1)]
                while currbuilding[0] == currbuilding[1]:
                    currbuilding[1] = buildings[random.randint(0, len(buildings)-1)]
            fromBuild = predict_building(currbuilding[0])
            toBuild = predict_building(currbuilding[1])
            res = "You chose navigating to " + toBuild[0]['buildingIntents'] + " building from " + fromBuild[0]['buildingIntents'] + " building. Is this correct?"
            confirmation = 1
        elif ints[0]['intent'] == "exit":
            res = getResponse(ints, intents)
            startNav = 0
            emergencyExit = 1
        elif startNav == 1:
            emergencyExit = 0
            res = "Please wait while the navigation is processing"
        else:
            emergencyExit = 0
            res = getResponse(ints, intents)
        ChatBox.insert(END, "Belatrix: " + res + '\n\n')

        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)


root = Tk()
root.title("Chatbot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

#import nlp dictionary
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('wordnet')

#Create Chat window
ChatBox = Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatBox.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="heart")
ChatBox['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(root, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#f9a602", activebackground="#3c9d9b",fg='#000000',
                    command= send )

#Create the box to enter message
EntryBox = Text(root, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatBox.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

root.mainloop()
