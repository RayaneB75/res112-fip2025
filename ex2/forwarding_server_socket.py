#!/usr/bin/env python3

"""A server module for the socket echo.
"""

import argparse
import socket
import select
import queue
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
server.listen(2)

inputs = [server]
outputs = []
messages = {}

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            messages[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print(f"Received {data.decode('utf-8')} from {address}")
                messages[s].put(data)
                outputs.append(s)
            else:
                print(f"Closing connection with {address}")
                inputs.remove(s)
                s.close()
    for s in writable:
        try:
            next_msg = messages[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            print(f"Sending {next_msg.decode('utf-8')} to {address}")
            s.send(next_msg)
    for s in exceptional:
        print(f"Closing connection with {address}")
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del messages[s]
