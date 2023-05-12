#!/usr/bin/env python3

"""A client module for the socket echo. It reads data from the keyboard and
sends it to a server.
"""

import argparse
import socket
import signal
import threading

#################################################
## Parsing command line arguments
parser = argparse.ArgumentParser(description='Echo Client')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    metavar="[1024-49151]", 
                    help='the server port number to connect to')
parser.add_argument("-m", "--machine", dest="host", type=str, default='localhost',
                    help="the server name or IP address to connect to")

options = parser.parse_args()

if options.port > 49151 or options.port < 1024:
    print("Invalid port: the port number has to be between 1024 and 49151")
    exit(1)


#################################################
## Global variables
s = None   # variable to store your socket


#################################################
## Handling of Ctrl+C
def close_connection(sig, frame):
    print('Ctrl+C Pressed. Closing the socket...')
    if s:
        # close the socket
        s.close()
    exit(0)

# Register this handler for Ctrl+C (SIGINT) event
signal.signal(signal.SIGINT, close_connection)


#################################################
## The main program
# Socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# Connection with the server
s.connect((options.host, options.port))

# Function to receive messages from the server
def receive_messages():
    while True:
        # Receive the data from the server
        data = s.recv(1024)
        if not data:
            break
        # Print the received message
        print("\nReceived:", data.decode("utf-8"))

# Start a separate thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

done = False
while not done:
    msg = "\nSend:"
    inputString = input(msg)
    if inputString in ("exit", "quit"):
        done = True
    else:
        # Encode the data (in UTF-8)
        inputString = inputString.encode("utf-8")
        # Send the data
        s.sendall(inputString)

# Wait for the receive thread to finish
receive_thread.join()

# Close the socket
s.close()
