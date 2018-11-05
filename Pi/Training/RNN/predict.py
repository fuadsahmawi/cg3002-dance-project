import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from keras.models import load_model

ALL_TEST = pickle.load(open("all_test", "rb"))

TEST_X = ALL_TEST[:, :, 0:(ALL_TEST.shape[2]-1)]
TEST_Y = ALL_TEST[:, :, -1]
TEST_Y = TEST_Y[:, 0]

# load model
model = load_model('rnn.h5')

# make prediction
y_pred = model.predict(TEST_X)

count = 0
y_pred_final = list()
for row in y_pred:
    predicted_class = np.argmax(row, axis=-1)
    proba = row[predicted_class]

    y_pred_final.append(predicted_class)
    
    if proba < 0.8:
        print(predicted_class)
        print(proba)
        count += 1

print(count)
        
acc = accuracy_score(TEST_Y, y_pred_final)
cm = confusion_matrix(TEST_Y, y_pred_final)
print(acc)
print(cm)