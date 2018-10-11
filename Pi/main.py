import serial
import time
import struct
import csv

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
    
    print(data)


    return data
    


# helper method to parse byte array from Arduino into integer array
def barray_to_intarray(b_array, n_bytes_per_int):
    int_array = []
    for i in range(0, len(b_array), n_bytes_per_int):
        int_data = int.from_bytes(b_array[i:i+n_bytes_per_int], byteorder='little')
        int_array.append(int_data)        
    return int_array

    

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


with open('data.csv', mode='w', newline='') as file:
	while True:
		# poll port for data packet
		packet = read_packet(ser)
		
		# in effect, if read_packet() does not return -1 or -2
		if not isinstance(packet, int):
			values = deserialize_packet(packet)
			
			file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			file_writer.writerow(values)

