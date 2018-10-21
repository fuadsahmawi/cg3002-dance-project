import struct
import sys
import time

import collections
from collections import Counter
import csv
import pickle
import serial

# constants
HANDSHAKE_INIT = (5).to_bytes(1, byteorder='big')
ACK = (6).to_bytes(1, byteorder='big')
NAK = (25).to_bytes(1, byteorder='big')
PACKET_SIZE = 81

# global variables
is_connected_to_mega = False

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
    
    for i in range(4): # loop 4 times for 4 sensors.
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
    
    checksum = int.from_bytes(packet[80:81], byteorder='big')
    
    # print("1:")
    # print(data[0:3])
    # print(data[3:6])
    print("2:")
    print(data[6:9])
    print(data[9:12])
    print("3:")
    print(data[12:15])
    print(data[15:18])
    # print("4:")
    # print(data[18:21])
    # print(data[21:24])
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
swm_model = None
rf_model = None
knn_model = None

decode_label_dict = {0:'chicken', 1:'number7', 2:'sidestep', 3:'wipers', 4:'turnclap'}
           
def init_models():
    knn_model = pickle.load(open("knn_model", 'rb'))
	svm_model = joblib.load("SVM.cls")
	rf_model = joblib.load("RanFor.cls")
            
def svm_pred(window_data):
    return svm_model.predict(window_data)
    
def rf_pred(window_data):
    return rf_model.predict(window_data)

def knn_pred(window_data):
    return knn_model.predict(window_data)
	
def extract_feature(window_data):
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
	
	return feature
    

def main_predict():
    ## TODO: encode window_size and window_slide_by in model itself?
    window_size = 40
    window_slide_by = 4
    
    ## https://stackoverflow.com/questions/4151320/efficient-circular-buffer
    window_data = collections.deque(maxlen=window_size)

    init_models()
    
    while True:
        # poll port for data packet
        packet = read_packet(ser)
        
        window_data.append(packet)
        count += 1
        
        if (window_data.size() == window_size and count == window_slide_by):
            extracted_features = extract_feature(window_data)
        
            vote1 = svm_pred(extracted_features)
            vote2 = rf_pred(extracted_features)
            vote3 = knn_pred(window_data)
            
            count = 0
            
            votes = Counter(vote1, vote2, vote3)
            final_vote = votes.most_common()
            
            # send_comms(decode_label_dict[final_vote])

def collect_data():
    # setup serial line
    ser = serial.Serial('COM4', 57600, timeout=1)
    print("connected to COM4\n")

    # handshake
    # while not is_connected_to_mega:
    #     ser.write(HANDSHAKE_INIT)
    #     data = ser.read(1)
    #     if data == ACK:
    #         ser.write(ACK)
    #         is_connected_to_mega = True


    with open(sys.argv[1], mode='w', newline='') as file:
        while True:
            # poll port for data packet
            packet = read_packet(ser)
            
            # in effect, if read_packet() does not return -1 or -2
            if not isinstance(packet, int):
                values = deserialize_packet(packet)
                values = values[6:18] # record sensor 2 and 3 data
                
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow(values)
        