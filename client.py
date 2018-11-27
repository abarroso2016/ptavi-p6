#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    SERVER = 'localhost'
    METHOD = sys.argv[1]
    BASH = sys.argv[2].split(":")
    SIP = BASH[0]
    PORT = int(BASH[1])
except IndexError:
    print("Usage: python3 client.py method receiver@IP:SIPport")
    sys.exit()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    LINE = METHOD + " " + SIP + " SIP/2.0\r\n"
    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))
    recibido = data.decode('utf-8').split(" ")
    if recibido[1] == '100':
        LINE = "ACK " + SIP + " SIP/2.0\r\n"
        print("Enviando: " + LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')

    
    print("Terminando socket...")

print("Fin.")
