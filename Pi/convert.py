# program converts a string into bytes into floats and integers
import struct



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
        
        
        acc_x = struct.unpack('f', packet[index: index + 4])
        index += 4
        data.append(acc_x)
        
        acc_y = struct.unpack('f', packet[index: index + 4])
        index += 4
        data.append(acc_y)
        
        acc_z = struct.unpack('f', packet[index: index + 4])
        index += 4
        data.append(acc_z)
       
    current = struct.unpack('f', packet[index: index + 4])
    data.append(current)
    index += 4
    
    voltage  =  struct.unpack('f', packet[index: index + 4])
    data.append(voltage)
    index += 4
    
    checksum = int.from_bytes(packet[80:81], byteorder='big')
    
    return data
    


# helper method to parse IMU byte array data into integer array
def barray_to_intarray(b_array, n_bytes_per_int):
    int_array = []
    for i in range(0, len(b_array), n_bytes_per_int):
        int_data = int.from_bytes(b_array[i:i+n_bytes_per_int], byteorder='big')
        int_array.append(int_data)        
    return int_array

# byte_array = bytes.fromhex('<SOME INPUT>')
# values_list = deserialize_packet(byte_array)


b_array = (500).to_bytes(2, byteorder='little')
int_data = int.from_bytes(b_array[0:2], byteorder='big')
print(int_data)