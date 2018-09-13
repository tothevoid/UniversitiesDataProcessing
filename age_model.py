import numpy as np
import keras
from keras.utils import np_utils 

model = keras.models.load_model('ages_model.h5')

size = 13
dataset = np.loadtxt("test_narfu.csv", delimiter=";", skiprows=1)
classes = 104

X, Y = dataset[:,0:size], dataset[:,size+1]
Y = np_utils.to_categorical(Y, classes)

scores = model.evaluate(X, Y, batch_size=128)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
