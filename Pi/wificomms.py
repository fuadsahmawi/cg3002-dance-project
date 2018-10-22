#!/usr/bin/env python

import socket

#from Crypto.Util import Padding # DOES NOT WORK
from Crypto import Random
from Crypto.Cipher import AES

from base64 import b64encode, b64decode



# copied the padding module here because import did not work
""" Functions to manage padding
This module provides minimal support for adding and removing standard padding
from data.
"""

all = [ 'ValueError', 'pad', 'unpad' ]

from Crypto.Util.py3compat import *


def pad(data_to_pad, block_size, style='pkcs7'):
    """Apply standard padding.
    :Parameters:
      data_to_pad : byte string
        The data that needs to be padded.
      block_size : integer
        The block boundary to use for padding. The output length is guaranteed
        to be a multiple of ``block_size``.
      style : string
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    :Return:
      The original data with the appropriate padding added at the end.
    """

    padding_len = block_size-len(data_to_pad)%block_size
    if style == 'pkcs7':
        padding = bchr(padding_len)*padding_len
    elif style == 'x923':
        padding = bchr(0)*(padding_len-1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0)*(padding_len-1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding

def unpad(padded_data, block_size, style='pkcs7'):
    """Remove standard padding.
    :Parameters:
      padded_data : byte string
        A piece of data with padding that needs to be stripped.
      block_size : integer
        The block boundary to use for padding. The input length
        must be a multiple of ``block_size``.
      style : string
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    :Return:
        Data without padding.
    :Raises ValueError:
        if the padding is incorrect.
    """

    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = bord(padded_data[-1])
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:]!=bchr(padding_len)*padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1]!=bchr(0)*(padding_len-1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bchr(128))
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len>1 and padded_data[1-padding_len:]!=bchr(0)*(padding_len-1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]


def tcp(MESSAGE):
    TCP_IP = '192.168.43.12'
    TCP_PORT = 2345
    BUFFER_SIZE = 100
    # MESSAGE = b"#mermaid | 4 | 0.1 | 0.4 | 6 |"
    SECRET_KEY = bytes("abcdefghijklmnop", 'utf-8')

    # connect to TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    # init cipher
    init_vect = Random.new().read(AES.block_size)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, init_vect)

    # encrypt with AES_CBC then encode w base64
    padded_message = pad(MESSAGE, AES.block_size)
    encoded_message = b64encode(init_vect + cipher.encrypt(padded_message))
    print(encoded_message)

    s.send(encoded_message)
    data = s.recv(BUFFER_SIZE)
    s.close()

    print ("received data: ", data)





