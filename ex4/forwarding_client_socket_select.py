#!/usr/bin/env python3

"""A client module for the socket echo. It reads data from the keyboard and
sends it to a server.
"""

import argparse
import socket
import signal
import select

#################################################
# Parsing command line arguments
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
# Global variables
s = None   # variable to store your socket


#################################################
# Handling of Ctrl+C
def close_connection(sig, frame):
    print('Ctrl+C Pressed. Closing the socket...')
    if s:
        # close the socket
        s.close()
    exit(0)


# Register this handler for Ctrl+C (SIGINT) event
signal.signal(signal.SIGINT, close_connection)


#################################################
# The main program
# Socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# Connection with the server
s.connect((options.host, options.port))

# Read from the keyboard input and send it to the server,
# and display the response from the server
while True:
    print("\nMoi: ", end="")
    readable, _, _ = select.select([s, 0], [], [])
    for r in readable:
        if r == s:
            data = s.recv(1024)
            if not data:
                print("Server closed the connection")
                exit(0)
            print(f"\nLui: {data.decode()}")
        else:
            data = input()
            s.send(data.encode())


# Close the socket
s.close()
