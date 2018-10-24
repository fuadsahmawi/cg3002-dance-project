import struct
import sys
import time
import pdb

import collections
from collections import Counter
import csv
import numpy as np
import pickle
import serial
from sklearn.externals import joblib

#import wificommms

# constants
HANDSHAKE_INIT = struct.pack("B", 5) # (5).to_bytes(1, byteorder='big') # 
ACK = struct.pack("B", 6) # (6).to_bytes(1, byteorder='big') # 
NAK = struct.pack("B", 25) # (25).to_bytes(1, byteorder='big')
PACKET_SIZE = 45

# global variables
is_connected_to_mega = False
current = 0
voltage = 0
power = 0
cumPower = 0

# debugging variables
debug = False # flag for printing debugging statements
k = 0


# pre-condition: last byte of data should be checksum
def read_packet(serial):
    
    if serial.in_waiting >= PACKET_SIZE :
        packet = serial.read(PACKET_SIZE)
        serial.reset_input_buffer()
        
        if checksum(packet) == packet[len(packet) - 1]:
            serial.write(ACK)
            # serial.reset_input_buffer()
            return packet # an array of bytes
        else:
            serial.write(NAK)
            return -1 # checksum issue
    else:
        return -2
    
def checksum(b_array):
    # check values
    csum = b_array[0]
    if len(b_array) < 2:
        raise ValueError('array must be more than size 1')
    else:        
        for i in range(1, len(b_array) - 1):
            csum = csum ^ b_array[i]        
    return csum

# pre-condition: packet must be PACKET_SIZE, and of pre-defined format
def deserialize_packet(packet):
    # returns a list of int, int, int, float, float, float etc then 2 floats
    # for current and voltage
    
    # beware that endianness of arduino is little endian
    # data is in byte form, but printed as ascii characters
    # (e.g. 0x21 -> !, 0x30 -> 0)
    # hence, do not print the byte array immediately or it will render as ascii symbols
    # instead, convert the required bytes to integers, then print or transfer)
    
    index = 0
    
    data = []
    
    for i in range(2): # loop 2 times for 2 sensors.
        gyro_data_array = barray_to_intarray(packet[index:index + 6], 2) # extract 3 ints from 6 bytes
        index += 6
        data.extend(gyro_data_array)
        
        
        acc_x = struct.unpack('f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_x)
        
        acc_y = struct.unpack('f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_y)
        
        acc_z = struct.unpack('f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_z)
       
    current = struct.unpack('f', packet[index: index + 4])[0]
    data.append(current)
    index += 4
    
    voltage  =  struct.unpack('f', packet[index: index + 4])[0]
    data.append(voltage)
    index += 4
    
    power = voltage * current
    # cumPower = energy
    
    checksum = int.from_bytes(packet[PACKET_SIZE-1:PACKET_SIZE], byteorder='big')
    
    if debug:
        #print("2:")
        #print(data[0:3])
        #print(data[3:6])

        #print("3:")
        #print(data[6:9])
        #print(data[9:12])

        print(current)
        print(voltage)
        print()

    return data
    


# helper method to parse byte array from Arduino into integer array
def barray_to_intarray(b_array, n_bytes_per_int):
    int_array = []
    for i in range(0, len(b_array), n_bytes_per_int):
        int_data = int.from_bytes(b_array[i:i+n_bytes_per_int], byteorder='big', signed = True)
        int_array.append(int_data)        
    return int_array

## global vars for main_predict()
mlp_model = None
rf_model = None
knn_model = None

decode_label_dict = {0:'neutral', 1:'wipers', 2:'number7', 3:'chicken', 4:'sidestep', 5:'turnclap'}

def init_models():
    #knn_model = joblib.load("knn_model")
    print(knn_model)
    print()
    
    mlp_model = joblib.load("MLP.cls")
    print(mlp_model)
    print()
    
    rf_model = joblib.load("RanFor.cls")
    print(rf_model)
    print()
    
    return knn_model, mlp_model, rf_model

def svm_pred(model, window_data):
    return model.predict(window_data)
    
def rf_pred(model, window_data):
    return model.predict(window_data)

def knn_pred(model, window_data):
    return model.predict(window_data)

def model_pred(model, window_data):
    return model.predict(window_data)
    
def extract_feature(window_data):
    window_data = np.array(window_data)

    feature = []
    meanAccX1 = window_data[:,3].mean()
    meanAccY1 = window_data[:,4].mean()
    meanAccZ1 = window_data[:,5].mean()
    meanAccX2 = window_data[:,9].mean()
    meanAccY2 = window_data[:,10].mean()
    meanAccZ2 = window_data[:,11].mean()
    meanGyrX1 = window_data[:,0].mean()
    meanGyrY1 = window_data[:,1].mean()
    meanGyrZ1 = window_data[:,2].mean()
    meanGyrX2 = window_data[:,6].mean()
    meanGyrY2 = window_data[:,7].mean()
    meanGyrZ2 = window_data[:,8].mean()
    feature.append(meanAccX1)
    feature.append(meanAccY1)
    feature.append(meanAccZ1)
    feature.append(meanGyrX1)
    feature.append(meanGyrY1)
    feature.append(meanGyrZ1)
    feature.append(meanAccX2)
    feature.append(meanAccY2)
    feature.append(meanAccZ2)
    feature.append(meanGyrX2)
    feature.append(meanGyrY2)
    feature.append(meanGyrZ2)
    
    peakAccX1 = window_data[:,3].max()
    peakAccY1 = window_data[:,4].max()
    peakAccZ1 = window_data[:,5].max()
    peakAccX2 = window_data[:,9].max()
    peakAccY2 = window_data[:,10].max()
    peakAccZ2 = window_data[:,11].max()
    peakGyrX1 = window_data[:,0].max()
    peakGyrY1 = window_data[:,1].max()
    peakGyrZ1 = window_data[:,2].max()
    peakGyrX2 = window_data[:,6].max()
    peakGyrY2 = window_data[:,7].max()
    peakGyrZ2 = window_data[:,8].max()
    feature.append(peakAccX1)
    feature.append(peakAccY1)
    feature.append(peakAccZ1)
    feature.append(peakAccX2)
    feature.append(peakAccY2)
    feature.append(peakAccZ2)
    feature.append(peakGyrX1)
    feature.append(peakGyrY1)
    feature.append(peakGyrZ1)
    feature.append(peakGyrX2)
    feature.append(peakGyrY2)
    feature.append(peakGyrZ2)
    
    return np.array(feature).reshape(1,-1)
    

def main_predict():
    ## TODO: encode window_size and window_slide_by in model itself?
    window_size = 40
    window_slide_by = 4
    
    ## https://stackoverflow.com/questions/4151320/efficient-circular-buffer
    window_data = collections.deque(maxlen=window_size)

    models = init_models()
    count = 0
    vote1 = 0
    vote2 = 0
    while True:
        # poll port for data packet
        ## assumed packet is list
        raw_packet = read_packet(ser)
        if not isinstance(raw_packet, int):
            packet = deserialize_packet(raw_packet)
            window_data.append(packet)
            count += 1

            if (len(window_data) == window_size and count >= window_slide_by):
                extracted_features = extract_feature(window_data)
                # MLP
                vote1 = model_pred(models[1], extracted_features)
                print("model[1]: ", decode_label_dict[vote1[0]])

                # Random Forest
                #vote2 = model_pred(models[2], extracted_features)
                #print("model[2]: ", decode_label_dict[vote2[0]])

                #vote3 = -1 #knn_pred(models[0], extracted_features)
                
                count = 0
                votes = Counter([vote1[0]]) #.astype(np.int64)
                final_vote = votes.most_common()

                if len(final_vote) >= 3: ## no decision
                    continue
                elif final_vote[0][0] == 0: ## if vote = neutral, don't send to server
                    print("neutral move detected")
                    continue
                else: ## Send data over TCP to evaluation server
                    print("final vote: ", decode_label_dict[final_vote[0][0]])
                    window_data.clear()
                    
                    #tcp(decode_label_dict[final_vote[0]] + '|' + voltage + '|' + current + '|' + power + '|' + cumPower + '|')


        
def collect_data():
    with open(sys.argv[1], mode='w', newline='') as file:
        while True:
            # poll port for data packet
            packet = read_packet(ser)
        # in effect, if read_packet() does not return -1 or -2
            if not isinstance(packet, int):
                values = deserialize_packet(packet)
                values = values[0:12] # record sensor 2 and 3 data
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow(values)


                
# ======== MAIN =========

# setup serial line
ser = serial.Serial('/dev/serial0', 57600, timeout=1)
print("connected to serial\n")

# handshake
while not is_connected_to_mega:
    ser.write(HANDSHAKE_INIT)
    data = ser.read(1)
    if data == ACK:
        ser.write(ACK)
        is_connected_to_mega = True
print("handshake passed")

#pdb.set_trace()

main_predict()
