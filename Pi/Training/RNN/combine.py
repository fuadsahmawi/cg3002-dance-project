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
    
    person_data = {}
    
    for file_name in filenames:        
        person_name = file_name[file_name.find("_")+1:file_name.find(".")]
        
        file_path = os.path.join(labelled_dir, file_name)
        file = read_csv(file_path)
                
        if person_name not in person_data:
            person_data[person_name] = np.array(file)
        else:
            person_data[person_name] = np.append(person_data[person_name], file, axis=0)
            
        print(person_name)
        print(type(person_data[person_name]))
        
    for key, value in person_data.items():
        file_path = os.path.join(combined_dir, key + ".csv")
        #np.savetxt(file_path, value, delimiter=",", fmt='%s')
        df = DataFrame(value, columns=headers)
        df.to_csv(file_path, index=False, header=True, sep=',')
    
    
    
    