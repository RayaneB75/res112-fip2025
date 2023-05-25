#!/usr/bin/env python3

"""A server module for the socket echo.
"""

import argparse
import socket
import signal

#################################################
## Parsing command line arguments
parser = argparse.ArgumentParser(description='Echo Server')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    metavar="[1024-49151]", 
                    help='the port number to bind to')

options = parser.parse_args()

if options.port > 49151 or options.port < 1024:
    print("Invalid port: the port number has to be between 1024 and 49151")
    exit(1)

#################################################
## Global variables
host = ''  # address to bind to. '' means all available interfaces
server = None   # variable to store your socket


#################################################
## Handling of Ctrl+C
def close_connection(sig, frame):
    print('Ctrl+C Pressed. Closing the socket...')
    if server:
        # close the socket
        server.close()
    exit(0)

# Register this handler for Ctrl+C (SIGINT) event
signal.signal(signal.SIGINT, close_connection)

#################################################
## The main program

# socket creation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# bind with a local address and port
server.bind((host, options.port))

# make it a server socket
server.listen(3)

clients = []

while True:
    for i in range(3):
        c, a = server.accept()
        clients.append(c)
        print(f"Connection from {a}")
        msg = f"Hello, client {i+1}!"
        c.sendall(msg.encode('utf-8'))
    
    while True:
        data = clients[0].recv(1024)
        if not data:
            print("Client closed the connection")
            break
        for c in clients[1:]:
            c.sendall(data)