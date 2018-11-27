#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    SONG = sys.argv[3]
except IndexError:
    print("Usage: python3 server.py IP port audio_file")
    sys.exit()


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        line = self.rfile.read()
        print("El cliente nos manda " + line.decode('utf-8'))
        prueba = line.decode('utf-8').split(" ")
        METHOD = prueba[0]
        if METHOD == "INVITE":
            self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
            self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        if METHOD == "ACK":
            aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + SONG
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
            print("Cancion enviada")
        if METHOD == "BYE":
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        if METHOD != "INVITE" and METHOD != "ACK" and METHOD != "BYE":
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
