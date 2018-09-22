from keras.models import Sequential
from keras.layers import Dense, Dropout, Input, concatenate, Flatten
import numpy as np
import keras
import tensorflow as tf
from keras.utils import np_utils 
from sklearn.model_selection import train_test_split
from sklearn import linear_model

size = 14
classes = 60
batch = 64

university = 'mgu'

male_test = np.loadtxt(university+'_age_male_test.csv', delimiter=",", skiprows=1)
female_test = np.loadtxt(university+'_age_female_test.csv', delimiter=",", skiprows=1)

X_m = male_test[:,0:size]
X_f = female_test[:,0:size]

Y = female_test[:,size+1]

X = list()

for index in range(len(male_test)):
    X.append((X_m[index], X_m[index]))

X_train, X_test, Y_train, Y_test = train_test_split(np.array(X), Y, test_size=0.2, random_state=42)

Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)

model = Sequential()
model.add(Dense(size*2, input_shape=(2,size), activation='relu')) 

model.add(Dense(size*4, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(size*4, activation='relu'))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(classes, activation='softmax'))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

model.fit(X_train, Y_train, epochs = 250, batch_size=batch)

scores = model.evaluate(X_test, Y_test, batch_size=batch)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

res = model.predict_classes(X_test)

model.save('model_predict_age_new.h5')