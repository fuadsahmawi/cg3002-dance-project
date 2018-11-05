import os
import sys
from pandas import DataFrame
from pandas import read_csv
import numpy as np
    
""" Get all files
    combine based on name
    output named files
"""

if __name__ == "__main__": 
    
    labelled_dir = os.path.join(os.getcwd(), 'labelled')
    combined_dir = os.path.join(os.getcwd(), 'combined')
    
    filenames = next(os.walk(labelled_dir))[2] ## get file (not dir) names only
    
    headers = ["gyrx1","gyry1", "gyrz1", "accx1", "accy1", "accz1", "gyrx2", "gyry2", "gyrz2", "accx2", "accy2", "accz2", "activity"]
    
    ben_csv = np.empty(shape=(0,13))
    melvin_csv = np.empty(shape=(0,13))
    yp_csv = np.empty(shape=(0,13))
    xinhui_csv = np.empty(shape=(0,13))
    fuad_csv = np.empty(shape=(0,13))
    eryao_csv = np.empty(shape=(0,13))
    
    person_data = {'ben':ben_csv, 'melvin':melvin_csv, 'yp':yp_csv, 'xh':xinhui_csv, 'fuad':fuad_csv, 'eryao':eryao_csv}
    
    for file_name in filenames:
        person_name = file_name.split('_')[1]
        person_name = person_name.split('.')[0]
        
        file_path = os.path.join(labelled_dir, file_name)
        file = read_csv(file_path)
        
        if person_data[person_name] is None:
            person_data[person_name] = file
        else:
            person_data[person_name] = np.append(person_data[person_name], file, axis=0)
        
    for key, value in person_data.items():
        file_path = os.path.join(combined_dir, key + ".csv")
        #np.savetxt(file_path, value, delimiter=",", fmt='%s')
        df = DataFrame(value, columns=headers)
        df.to_csv(file_path, index=False, header=True, sep=',')
    
    
    
    