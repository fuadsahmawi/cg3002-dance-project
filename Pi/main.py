import math
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
from pandas as pd
from sklearn.preprocessing import StandardScaler

#import wificomms

# constants
HANDSHAKE_INIT = struct.pack("B", 5) # (5).to_bytes(1, byteorder='big') # 
ACK = struct.pack("B", 6) # (6).to_bytes(1, byteorder='big') # 
NAK = struct.pack("B", 25) # (25).to_bytes(1, byteorder='big')
PACKET_SIZE = 49
WAITING_TIME = 0
REACTION_TIME = 1

# global variables
is_connected_to_mega = False
current = 0
voltage = 0
power = 0
cumPower = 0

# debugging variables
debug = True # flag for printing debugging statements
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
    global current;
    global voltage;
    global power;
    global cumPower;
    index = 0

    data = []

    for i in range(2): # loop 2 times for 2 sensors.
        gyro_data_array = barray_to_intarray(packet[index:index + 6], 2) # extract 3 ints from 6 bytes
        index += 6
        data.extend(gyro_data_array)

        acc_x = struct.unpack_from('<f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_x)

        acc_y = struct.unpack_from('<f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_y)

        acc_z = struct.unpack_from('<f', packet[index: index + 4])[0]
        index += 4
        data.append(acc_z)

    current = struct.unpack_from('<f', packet[index: index + 4])[0]
    current = current * 1000 # convert to mA
    #data.append(current)
    index += 4

    voltage  =  struct.unpack_from('<f', packet[index: index + 4])[0]
    #data.append(voltage)
    index += 4

    cumPower = struct.unpack_from('<f', packet[index: index+4])[0]
    #data.append(cumPower)
    index +=4

    power = voltage * current

    checksum = int.from_bytes(packet[PACKET_SIZE-1:PACKET_SIZE], byteorder='big')

    if debug:
        print("sensor 1:")
        print(data[0:3])
        print(data[3:6])

        print("sensor 2:")
        print(data[6:9])
        print(data[9:12])

        print("current: ", current)
        print("voltage: ", voltage)
        print("power: ", power)
        print("cumPower: ", cumPower)
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

decode_label_dict = {0:'neutral', 1:'wipers', 2:'number7', 3:'chicken', 4:'sidestep', 5:'turnclap', 6:'number6', 7:'salute', 8:'mermaid', 9:'swing', 10:'cowboy', 11:'bow'}

def init_models():
    svm_model = joblib.load("SVM.cls")
    print(svm_model)
    print()

    mlp_model = joblib.load("MLP.cls")
    print(mlp_model)
    print()

    rf_model = joblib.load("RanFor.cls")
    print(rf_model)
    print()

#    knn_model = pickle.load(open("knn_model", "rb"))
#    print(knn_model)
#    print()

    return svm_model, mlp_model, rf_model #, knn_model

def model_pred(model, window_data):
    all_probas = model.predict_proba(window_data)
    
    predicted_class = np.argmax(all_probas, axis=-1)
    proba = all_probas[predicted_class]
    
    if proba > 0.8:
        return predicted_class
    else:
        return -1

def extract_feature(window_data):
    window_data = pd.DataFrame(window_data)
	
	meanData = window_data.mean()
	peak = window_data.max()
	Q3 = window_data.quantile(0.75)
    Q1 = window_data.quantile(0.25)
	iqr = Q3 - Q1
	
	feature = feature.append(meanData, ignore_index = True)
	feature = feature.append(peak, ignore_index = True)
	feature = feature.append(iqr, ignore_index = True)
	
	scaler = StandardScaler()
	scaler.fit(feature)
	feature = scaler.transform(feature)

    return feature


def main_predict():
    global current;
    global voltage;
    global power;
    global cumPower;
    ## TODO: encode window_size and window_slide_by in model itself?
    window_size = 40
    window_slide_by = 4

    ## https://stackoverflow.com/questions/4151320/efficient-circular-buffer
    window_data = collections.deque(maxlen=window_size)

    models = init_models()
    time.sleep(WAITING_TIME) # wait for server to start receiving moves

    count = 0
    vote0 = 0
    vote1 = 0
    vote2 = 0
    nan_flag = 0
    while True:
        # poll port for data packet
        ## assumed packet is list
        raw_packet = read_packet(ser)

        if not isinstance(raw_packet, int):
            #print("raw bytes: ", raw_packet)
            #print("".join(format(x, '02x') for  x in raw_packet))
            #print()
            packet = deserialize_packet(raw_packet)
            for value in packet:
                if str(value) == 'nan':
                    print('nan detected')
                    nan_flag = 1

            if not nan_flag:
                window_data.append(packet)
                count += 1
            else:
                nan_flag = 0
                continue

            if (len(window_data) == window_size and count >= window_slide_by):
                extracted_features = extract_feature(window_data)
                print(extracted_features)

                # SVM
                vote0 = model_pred(models[0], extracted_features)
                print("model[0]: ", decode_label_dict[vote0])
                
                # MLP
                vote1 = model_pred(models[1], extracted_features)
                print("model[1]: ", decode_label_dict[vote1])

                # Random Forest
                vote2 = model_pred(models[2], extracted_features)
                print("model[2]: ", decode_label_dict[vote2])

#                vote3 = model_pred(models[3], extracted_features)
#                print("knn", decode_label_dict[vote3[0]])

                count = 0
                votes = Counter([vote0, vote1, vote2]) #.astype(np.int64)
                vote_list = votes.most_common()
                final_vote = vote_list[0][0]

                if len(vote_list) >= 3 or final_vote == -1: ## no decision or probabilities too low
                    continue
                elif vote0 == 0: ## if vote = neutral, don't send to server
                    print("vote[0]: neutral move detected\n")
                    window_data.clear()
                    continue
                else: ## Send data over TCP to evaluation server
                    print("final vote: ", decode_label_dict[final_vote], "\n")
                    window_data.clear()

                    #print(voltage)
                    #print(current)
                    MESSAGE = bytes("#" + decode_label_dict[final_vote] + "|" + str(voltage) + "|" + str(current) + "|" + str(power) + "|" + str(cumPower) + "|", 'utf-8')

                    #wificomms.tcp(MESSAGE)
                    time.sleep(1.5) # give time for reaction


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
    print("attempting handshake")
    ser.write(HANDSHAKE_INIT)
    data = ser.read(1)
    if data == ACK:
        ser.write(ACK)
        is_connected_to_mega = True
    ser.reset_input_buffer()
print("handshake passed")

# wificomms.tcp_init()

#time.sleep(WAITING_TIME + REACTION_TIME)

#pdb.set_trace()

main_predict()
