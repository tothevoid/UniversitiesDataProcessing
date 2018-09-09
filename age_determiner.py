import helpers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np
import keras
import tensorflow as tf
import helpers
from keras.utils import np_utils 
import vk_api 

# config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 4} ) 
# sess = tf.Session(config=config) 
# keras.backend.set_session(sess)

size = 13
classes = 60

dataset = np.loadtxt("test.csv", delimiter=";", skiprows=1)
valid = np.loadtxt("bdays_new.csv", delimiter=",", skiprows=1)
#validation
X, Y = dataset[:,0:size], dataset[:,size+1]
X_test =  valid[:,0:size]

X = X.astype('float32') 
Y = np_utils.to_categorical(Y)
X_test = X_test.astype('float32') 

model = Sequential()
model.add(Dense(size*2, input_dim=size, activation='relu')) 

model.add(Dense(size*2, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(size*2, activation='linear'))
model.add(Dropout(0.2))


model.add(Dense(classes, activation='softmax'))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(X, Y, epochs = 100, batch_size=128)
res = model.predict_classes(X_test)

scores = model.evaluate(X, Y, batch_size=128)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

full_res = list()

from numpy import argmax

for i in range(len(X_test)):
    val = X_test[i]
    row = np.append(val, res[i])
    full_res.append(row)
    #print(argmax(np_utils.to_categorical(res[i], classes)))
    #print("X=%s, Predicted=%s\n" % (X_test[i], res[i]+22))

np.savetxt("predict.csv", full_res, delimiter=",",  encoding='utf-8')