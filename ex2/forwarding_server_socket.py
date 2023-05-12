#!/usr/bin/env python3

"""A server module for the socket echo.
"""

import os
import argparse
import socket
import signal
import threading

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
s = None   # variable to store your socket
connections = []  # list to store client connections

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

# Bind with a local address and port
s.bind((host, options.port))

# Make it a server socket
s.listen(2)

# Function to handle individual client connections
def handle_client_connection(conn):
    while True:
        # Receive the data
        data = conn.recv(1024)
        if not data:
            break
        # Forward the message to the other client
        for connection in connections:
            if connection != conn:
                connection.send(data)
    # Close the connection
    conn.close()

# Function to accept client connections
def accept_connections():
    for i in range(2):
        # Wait for a connection
        conn, addr = s.accept()
        # Add the connection to the list
        connections.append(conn)
        # Start a new thread to handle the client connection
        threading.Thread(target=handle_client_connection, args=(conn,)).start()

# Start accepting client connections
accept_connections()
