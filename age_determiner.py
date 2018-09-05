import helpers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np
import keras
import tensorflow as tf
import helpers

# config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 4} ) 
# sess = tf.Session(config=config) 
# keras.backend.set_session(sess)

size = 13

dataset = np.loadtxt("validation.csv", delimiter=",", skiprows=1)
valid = np.loadtxt("test.csv", delimiter=",", skiprows=1)

X, Y = dataset[:,0:size], dataset[:,size+1]
X_test =  valid[:,0:size]

X = X.astype(int)
Y = Y.astype(int)
X_test = X_test.astype(int)

model = Sequential()
model.add(Dense(size*2, input_dim=size, activation='relu')) 

model.add(Dense(size*2, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(size*2, activation='linear'))
model.add(Dropout(0.2))


model.add(Dense(1, activation='relu'))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
 
model.fit(X, Y, epochs = 100, batch_size=128)
res = model.predict(X_test)

#scores = model.evaluate(X_test, Y_test, batch_size=150)
#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

full_res = list()

for i in range(len(X_test)):
    val = X_test[i]
    row = np.append(val, res[i])
    full_res.append(row)
    #print("X=%s, Predicted=%s\n" % (X_test[i], res[i]))

np.savetxt("predict.csv", full_res, delimiter=",",  encoding='utf-8')