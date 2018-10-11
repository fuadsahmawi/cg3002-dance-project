#!/usr/bin/env python

import socket
from Crypto.Cipher import AES
import base64
import sys
import os


TCP_IP = '192.168.43.117'
TCP_PORT = 2345
BUFFER_SIZE = 100  # Normally 1024, but we want fast response
KEY = "abcdefghijklmnop"

def decryptText(cipherText, Key):
        decodedMSG = base64.b64decode(cipherText)
        #print(decodedMSG)
        iv = decodedMSG[:16]
        #print(iv)
        secret_key = bytes(str(Key), encoding = "utf8")
#       secret_key = base64.b64decode(Key)
        cipher = AES.new(secret_key,AES.MODE_CBC,iv)
        decryptedText = cipher.decrypt(decodedMSG[16:]).strip()
        decryptedTextStr = decryptedText.decode('utf8')
        decryptedTextStr1 = decryptedTextStr[decryptedTextStr.find('#'):] 
        decryptedTextFinal = bytes(decryptedTextStr1[1:],'utf8').decode('utf8')
        action = decryptedTextFinal.split('|')[0]
        voltage = decryptedTextFinal.split('|')[1]
        current = decryptedTextFinal.split('|')[2]
        power = decryptedTextFinal.split('|')[3]
        cumpower = decryptedTextFinal.split('|')[4]
        return {'action': action, 'voltage': voltage, 'current': current, 'power': power, 'cumpower': cumpower}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print( 'Connection address:'), addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print ("received data:", data)
    decrypted = decryptText(data, KEY)
    print(decrypted)
    conn.send(data)  # echo
conn.close()
s.close()