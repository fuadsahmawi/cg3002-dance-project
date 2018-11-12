import numpy as np
import pandas as pd
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
        #print(predicted_class)
        #print(proba)
        count += 1

print(str(count) + " predictions have probability < 0.8")
        
acc = accuracy_score(TEST_Y, y_pred_final)

#rev_label_dict = {0:'neutral', 1:'wipers', 2:'num7', 3:'chicken', 4:'sidestep', 5:'turnclap', 6:'num6', 7:'salute', 8:'mermaid', 9:'swing', 10:'cowboy', 11:'bow'}

## removed neutral
rev_label_dict = {0:'wipers', 1:'num7', 2:'chicken', 3:'sidestep', 4:'turnclap', 5:'num6', 6:'salute', 7:'mermaid', 8:'swing', 9:'cowboy', 10:'bow'}
labels = list(rev_label_dict.values())

## convert int to strings
TEST_Y = [rev_label_dict[y] for y in TEST_Y]
y_pred_final = [rev_label_dict[y] for y in y_pred_final]

#cm = confusion_matrix(TEST_Y, y_pred_final)
cm = pd.DataFrame(confusion_matrix(TEST_Y, y_pred_final, labels), index=labels, columns=labels)

print(acc)
print(cm)
