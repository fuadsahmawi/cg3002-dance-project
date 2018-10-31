import sys
import pickle
import numpy as np
import pandas as pd
from pandas import concat
from pandas import unique
from pandas import read_csv
from pandas import DataFrame
from sklearn.model_selection import train_test_split
 
def truncate(data, window_size=100):
    """ Function truncates data if num_rows > window_size
        
        Note: currently unused
    """
    
    num_data_to_drop = data.shape[0] % window_size
    if num_data_to_drop == 0:
        return data
        
    data = data[:-num_data_to_drop]
    
    return data

def reshape(data, window_size=100, num_features=3):
    """
        Function reshapes data from long to wide, including label at end of row
        
        Returns ndarray of shape ( _ , window_size*num_features + 1 )
        
        Note: currently unused
        
        DONE: Check that data is properly reshaped
    """

    arrs = list()
    
    for idx in range(data.shape[0] // window_size):    
        tmp = (data.values[idx*window_size : ((idx+1)*window_size), 3:6])
        tmp = tmp.reshape(window_size*num_features)
        ## include label in each row
        tmp = np.append(tmp, data.values[idx*window_size, 1])
        arrs.append(tmp)
    
    ## https://stackoverflow.com/questions/21322564/numpy-list-of-1d-arrays-to-2d-array
    return np.array(arrs)
 
def series_to_supervised(data, n_in, shift_by, n_out=0, dropnan=True):
    """ 
        Function converts series to supervised learning

        data: data to convert
        n_in: window_size
        shift_by: how much to shift window by
        n_out: output data label to forecast (we don't need)
        
        DONE: change overlap to fn param instead of current shift=1
        - retain every nth row
        
    """
    
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        ## https://stackoverflow.com/questions/10982089/how-to-shift-a-column-in-pandas-dataframe#10982198
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
        
    ## retain every shift_by(th) row    
    agg = agg.iloc[::shift_by, :]
        
    return agg
 
def get_overlapping_windows(label, data, timesteps, shift_by, dropnan=True):
    windows = series_to_supervised(data=data, n_in=timesteps, shift_by=shift_by, n_out=0, dropnan=dropnan)
    
    ## add col 'label' to pandas dataframe
    windows['label'] = int(label)

    return windows
 
def gen_int_files(df_list):
    """
        Function generates intermediate files (each activity in a file) for Avas
    """

    tmp_df = np.concatenate(df_list)
    activity_list = unique(tmp_df[:, label_col_initial])
    activity_list = [a for a in activity_list if isinstance(a, str)]
    for a in activity_list:
        tmp = tmp_df[tmp_df[:, label_col_initial] == a, :]
        np.savetxt(a + ".csv", tmp, delimiter=",", fmt='%s') 
 
## load dataset from each person
## note: if separate session (same person and move), save as different 'person'
df_list = list()
df_list.append(read_csv('ben.csv', header=0, index_col=None))
df_list.append(read_csv('eryao.csv', header=0, index_col=None))
df_list.append(read_csv('fuad.csv', header=0, index_col=None))
df_list.append(read_csv('melvin.csv', header=0, index_col=None))
df_list.append(read_csv('xinhui.csv', header=0, index_col=None))
df_list.append(read_csv('yp.csv', header=0, index_col=None))

data_col_start = 0
data_col_end = 12
timestep = 30
win_shift_amt = timestep // 10 # 90% overlap
label_col_initial = data_col_end
label_col = data_col_end*timestep

##gen_int_files(df_list)

## cut data into chunks of window_size per person so that data won't overlap between persons
all_data = list()
for idx, df in enumerate(df_list):

    activity_list = unique(df['activity'])
    print(activity_list)
    arrs = list()
    for a in activity_list:
        activity_dataset = df[df.activity == a]
        if activity_dataset.shape[0] > timestep:
            #arrs.append(reshape(truncate(activity_dataset)))
            arrs.append(get_overlapping_windows(label=a, data=activity_dataset.ix[:, data_col_start:data_col_end], timesteps=timestep, shift_by=win_shift_amt))
            
    cleaned_person = np.concatenate(arrs)
    all_data.append(cleaned_person)
 
dataset = np.concatenate(all_data)

## sort by last col aka activity type
dataset = np.array(sorted(dataset, key=lambda a_entry: a_entry[-1]))
print(dataset.shape)

activity_list = unique(dataset[:, label_col])

## get minimum number of data amongst activities
min = sys.maxsize
for a in activity_list:
    num_rows_in_activity = len(dataset[dataset[:, label_col] == a, :])
    print(str(a) + " " + str(num_rows_in_activity))
    if (min > num_rows_in_activity):
        min = num_rows_in_activity

print(min)

## all activities have same number of rows of data
all_train = list()
all_test = list()
for a in activity_list:
    tmp = dataset[dataset[:, label_col] == a, :] ## all rows of a
    tmp = tmp[0:min]                             ## reduce rows of a if needed
    
    ## TODO: split before segmenting, else introduces bias if train[0:30], test[15:30]
    ## train, test data overlaps
    train, test = train_test_split(tmp)
    all_train.append(train)
    all_test.append(test)

all_train = np.concatenate(all_train)
all_test = np.concatenate(all_test)
        
print(all_train[0:5])
print(all_test[0:5])
        
np.savetxt("train.csv", all_train, delimiter=",", fmt='%s')
np.savetxt("test.csv", all_test, delimiter=",", fmt='%s')

num_features = data_col_end

## shuffle data
np.random.shuffle(all_train)

X_train = np.empty(shape=(all_train.shape[0], timestep, num_features))
y_train = []

row_3d = []
## for each row
for row in all_train:
    
    ## get every num_features elements
    row_2d = []
    for i in range(timestep):
        row_2d.append(row[i:i+num_features])
        
    row_2d = np.array(row_2d)
    row_3d.append(row_2d)
    
    y_train.append(row[-1])

X_train = np.array(row_3d)    
print(X_train.shape)
print(len(y_train))

pickle.dump(X_train, open("X_train", 'wb'))
pickle.dump(y_train, open("y_train", 'wb'))