import os
import sys
from pandas import read_csv

#label_dict = {'neutral':0, 'wipers':1, 'num7':2, 'chicken':3, 'sidestep':4, 'turnclap':5, 'num6':6, 'salute':7, 'mermaid':8, 'swing':9, 'cowboy':10,'bow':11}

## removed neutral
label_dict = {'wipers':0, 'num7':1, 'chicken':2, 'sidestep':3, 'turnclap':4, 'num6':5, 'salute':6, 'mermaid':7, 'swing':8, 'cowboy':9, 'bow':10}

def label_csv(csv_input, labelled_value, csv_output):
    df = read_csv(csv_input, index_col=None)

    ## label last col
    df.insert(df.shape[1], labelled_value, labelled_value)
    
    df.to_csv(csv_output, sep=',', index=False)
    
if __name__ == "__main__":    
    unlabelled_dir = os.path.join(os.getcwd(), 'raw_data')
    labelled_dir = os.path.join(os.getcwd(), 'labelled')
    
    filenames = next(os.walk(unlabelled_dir))[2] ## get file (not dir) names only
    
    for file_name in filenames:
        dance_move = file_name.split('_')[0]
        
        print(dance_move)

        if dance_move in label_dict:
            csv_input = os.path.join(unlabelled_dir, file_name)
            csv_output = os.path.join(labelled_dir, file_name)
            label_csv(csv_input, label_dict[dance_move], csv_output)
        else:
            print("dance move not in label_dict")
            
    print("done")
    