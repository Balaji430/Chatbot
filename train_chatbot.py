## for word vectorizer
import nltk
from nltk.stem import WordNetLemmatizer

## for file operation
import json
import pickle

## for neural network
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random


## let code
# Step-1
lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []

ignore_words = ['?','!']

data_file = open('intents.json').read()
json_file = json.loads(data_file)

# # Step-2
for intent in json_file['intents']:
	for pattern in intent['patterns']:

		## tokenize each word
		w = nltk.word_tokenize(pattern)
		words.extend(w)

		## add documents in the corpus
		documents.append((w,intent['tag']))

		## add to our classes list
		if intent['tag'] not in classes:
			classes.append(intent['tag'])


## lemmatize , lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# sort classes
classes = sorted(list(set(classes)))

# docments = combination b/w patterns and intenets
print(len(documents),"documents")
#classes = intents
print(len(classes),"classes",classes)

# words = all words, vocabulary
print(len(words),"unique lemmatized words",words)

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))



## Step 3 - Creating a train and test data

## create our training data
training = []
## creating an empty array for our output
output_empty = [0] * len(classes)

## training set , bag of words for each sentence
for doc in documents:
	#initialize the bag of words
	bag = []
	#list of tokenized words for the pattern
	pattern_words = doc[0]
	#lemmatize each word- create base word , in attempt to represent related words
	pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

	# create our bag  of words array with 1, if word match found in current pattern

	for w in words:
		bag.append(1) if w in pattern_words else bag.append(0)

	# output is a '0' for each tag and '1' for current tag(for each pattern)
	output_row = list(output_empty)
	output_row[classes.index(doc[1])] = 1

	training.append([bag,output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

## Create train and test list . X - patterns , Y- intents

train_x = list(training[:,0])
train_y = list(training[:,1])

print("Training data created")

##Step-4 Build A Model

# create model - 3 layers.
# First layer 128 neurons,
# Second layer 64 neurons and
# Third output layer contains number of neurons equal to number of intents to predict output with softmax

model = Sequential()
model.add(Dense(128,input_shape = (len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

##Compile model.Stochastic Gradient Descent with Nestrov Accelarated Gradient gives good result
sgd = SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5,verbose=1)

model.save('chatbot_model.h5',hist)

print("model created")


## Refrrence Link for SGD: 'https://keras.io/api/optimizers/sgd/'