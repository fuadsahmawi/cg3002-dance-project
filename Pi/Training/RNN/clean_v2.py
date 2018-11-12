import os
import pickle
import numpy as np
from pandas import unique
from pandas import read_csv
from sklearn.model_selection import train_test_split
def overlap_data(data, window_size, win_shift_amt):
    """ input 2d array (timesteps, features)
        output 3d array (samples, timesteps, features)
    """
    num_rows = data.shape[0]
    num_features = data.shape[1]
    num_windows = (num_rows - window_size) // win_shift_amt
    array_3d = np.empty(shape=(num_windows, window_size, num_features))
    for start_idx in range(num_windows):
        window = data[start_idx: start_idx + window_size]
        array_3d[start_idx] = window
    return array_3d
    
## Sampling rate: 55 Hz
    
WINDOW_SIZE = 110 #2s window
WIN_SHIFT_AMT = WINDOW_SIZE // 10 # 90% overlap
NUM_FEATURES = 12

## load dataset from each person
## note: if separate session (same person and move), save as different 'person'

ALL_TRAIN = np.empty(shape=(0, WINDOW_SIZE, NUM_FEATURES+1))
ALL_VALIDATE = np.empty(shape=(0, WINDOW_SIZE, NUM_FEATURES+1))
ALL_TEST = np.empty(shape=(0, WINDOW_SIZE, NUM_FEATURES+1))

combined_dir = os.path.join(os.getcwd(), 'combined')
filenames = next(os.walk(combined_dir))[2] ## get file (not dir) names only

## cut data into chunks of window_size per person so that data won't overlap between persons
for filename in filenames:
    file_path = os.path.join(combined_dir, filename)
    df = read_csv(file_path, header=0, index_col=None)

    activity_list = unique(df['activity'])
    for a in activity_list:
        activity_dataset = df[df.activity == a]
        ## truncate data
        truncated_rows = activity_dataset.shape[0] - (activity_dataset.shape[0] % WINDOW_SIZE)
        activity_dataset = activity_dataset[0:truncated_rows]
        ## split data
        train, test = train_test_split(activity_dataset, shuffle=False, test_size=0.2)
        train, validate = train_test_split(train, shuffle=False, test_size=0.2)
        ## overlap data
        overlapped_train = overlap_data(train, WINDOW_SIZE, WIN_SHIFT_AMT)
        overlapped_validate = overlap_data(validate, WINDOW_SIZE, WIN_SHIFT_AMT)
        overlapped_test = overlap_data(test, WINDOW_SIZE, WIN_SHIFT_AMT)
        ## append it to all_
        ALL_TRAIN = np.concatenate((ALL_TRAIN, overlapped_train), axis=0)
        ALL_VALIDATE = np.concatenate((ALL_VALIDATE, overlapped_validate), axis=0)
        ALL_TEST = np.concatenate((ALL_TEST, overlapped_test), axis=0)
        
print(ALL_TRAIN.shape)
print(ALL_VALIDATE.shape)
print(ALL_TEST.shape)

pickle.dump(ALL_TRAIN, open("all_train", 'wb'))
pickle.dump(ALL_VALIDATE, open("all_validate", 'wb'))
pickle.dump(ALL_TEST, open("all_test", 'wb'))
