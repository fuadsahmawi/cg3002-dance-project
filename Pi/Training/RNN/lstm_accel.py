import sys
import numpy as np
import pickle
from math import sqrt
from numpy import concatenate
from pandas import unique
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation
from keras.utils import to_categorical
from keras.optimizers import Adam

## Sampling rate: 20Hz (1 sample every 50ms)

ALL_TRAIN = pickle.load(open("all_train", "rb"))
ALL_VALIDATE = pickle.load(open("all_validate", "rb"))
ALL_TEST = pickle.load(open("all_test", "rb"))

## https://stackoverflow.com/questions/45581243/how-to-delete-column-in-3d-numpy-array
TRAIN_X = ALL_TRAIN[:, :, 0:(ALL_TRAIN.shape[2]-1)]
TRAIN_Y = ALL_TRAIN[:, :, -1] ## get axis=2 last col
TRAIN_Y = TRAIN_Y[:, 0] ## get axis=1 first col

VALIDATE_X = ALL_VALIDATE[:, :, 0:(ALL_VALIDATE.shape[2]-1)]
VALIDATE_Y = ALL_VALIDATE[:, :, -1]
VALIDATE_Y = VALIDATE_Y[:, 0]

TEST_X = ALL_TEST[:, :, 0:(ALL_TEST.shape[2]-1)]
TEST_Y = ALL_TEST[:, :, -1]
TEST_Y = TEST_Y[:, 0]

NUM_ACTIVITIES = len(np.unique(TRAIN_Y))
TRAIN_Y = to_categorical(TRAIN_Y, num_classes=NUM_ACTIVITIES)
VALIDATE_Y = to_categorical(VALIDATE_Y, num_classes=NUM_ACTIVITIES)

# design network
model = Sequential()
## define LSTM with 50 neurons in the first hidden layer and 1 neuron in the output layer 
model.add(LSTM(50, input_shape=(TRAIN_X.shape[1], TRAIN_X.shape[2])))
model.add(Dense(NUM_ACTIVITIES))
model.add(Activation('softmax'))
model.compile(loss='mae', optimizer='adam')

# fit network
## batch size = (data sent in per iteration, until entire dataset = 1 epoch)
history = model.fit(x=TRAIN_X, y=TRAIN_Y, validation_data=(VALIDATE_X, VALIDATE_Y), epochs=30, verbose=2, shuffle=True)

# make prediction
y_pred = model.predict(TEST_X)
y_pred = np.argmax(y_pred,axis=-1)

acc = accuracy_score(TEST_Y, y_pred)
cm = confusion_matrix(TEST_Y, y_pred)
print(acc)
print(cm)

model.save("rnn.h5")

"""
TODO: visualize overlapped data (esp wipers, chicken high error)
TODO: loss decreases but val_loss stable
DONE: make rnn output categorical labels
- last layer outputs softmax probabilities
DONE: extend to 6 categories
DONE: output classification accuracy
DONE: output confusion matrix
DONE: visualize acc data (eg. x axis vs time), compare across activity types
- use equal amounts of data for each activity
DONE: split classes of data into 6 csv files, ensure data is same after

NOTE: senior used 15 min of training data per activity
"""