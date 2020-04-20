import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

building_words=[]
buildings = []
documents = []
ignore_letters = ['!', '?', ',', '.']
buildingIntents_file = open('buildingIntents.json').read()
buildingIntents = json.loads(buildingIntents_file)

# download nltk resources
nltk.download('punkt')
nltk.download('wordnet')

for intent in buildingIntents['intents']:
    for pattern in intent['patterns']:
        #tokenize each word
        word = nltk.word_tokenize(pattern)
        building_words.extend(word)
        #add documents in the corpus
        documents.append((word, intent['tag']))
        # add to our buildings list
        if intent['tag'] not in buildings:
            buildings.append(intent['tag'])
print(documents)
# lemmaztize and lower each word and remove duplicates
building_words = [lemmatizer.lemmatize(w.lower()) for w in building_words if w not in ignore_letters]
building_words = sorted(list(set(building_words)))
# sort buildings
buildings = sorted(list(set(buildings)))
# documents = combination between patterns and buildingIntents
print (len(documents), "documents")
# buildings = buildingIntents
print (len(buildings), "buildings", buildings)
# building_words = all building_words, vocabulary
print (len(building_words), "unique lemmatized building_words", building_words)

pickle.dump(building_words,open('building_words.pkl','wb'))
pickle.dump(buildings,open('buildings.pkl','wb'))

# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(buildings)
# training set, bag of building_words for each sentence
for doc in documents:
    # initialize our bag of building_words
    bag = []
    # list of tokenized building_words for the pattern
    pattern_building_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related building_words
    pattern_building_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_building_words]
    # create our bag of building_words array with 1, if word match found in current pattern
    for word in building_words:
        bag.append(1) if word in pattern_building_words else bag.append(0)
        
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[buildings.index(doc[1])] = 1
    
    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - buildingIntents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Buildings Training data created")

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of buildingIntents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('buildings_model.h5', hist)

print("building model created")
