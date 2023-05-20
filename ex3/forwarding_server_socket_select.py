#!/usr/bin/env python3

"""A server module for the socket echo.
"""

import argparse
import socket
import select
import queue
import signal

#################################################
# Parsing command line arguments
parser = argparse.ArgumentParser(description='Echo Server')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    metavar="[1024-49151]",
                    help='the port number to bind to')

options = parser.parse_args()

if options.port > 49151 or options.port < 1024:
    print("Invalid port: the port number has to be between 1024 and 49151")
    exit(1)

#################################################
# Global variables
host = ''  # address to bind to. '' means all available interfaces
server = None   # variable to store your socket


#################################################
# Handling of Ctrl+C
def close_connection(sig, frame):
    print('Ctrl+C Pressed. Closing the sockets...')
    for s in sockets:
        s.close()
    exit(0)


# Register this handler for Ctrl+C (SIGINT) event
signal.signal(signal.SIGINT, close_connection)

#################################################
# The main program

# socket creation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# bind with a local address and port
server.bind((host, options.port))

# make it a server socket
server.listen(2)

sockets = [server]

client_sockets = {}  # Dictionnaire pour associer les sockets clients à leurs ID
id = 0

while True:
    readable, _, _ = select.select(sockets, [], [])
    for s in readable:
        if s is server:
            connection, addr = server.accept()
            sockets.append(connection)
            id += 1
            # Associer le socket client à son ID
            client_sockets[connection] = id

            print(f"Connection from {addr} with id {id}")
            connection.sendall(f'Hello, client {id}!'.encode('utf-8'))
        else:
            data = s.recv(1024)
            if data:
                # Obtenir l'ID du client à partir de son socket
                client_id = client_sockets[s]

                print(
                    f"Received data from client {client_id}: {data.decode('utf-8')}")
                for c in client_sockets:
                    if c is not server and c is not s:
                        c.sendall(data)
            else:
                # Obtenir l'ID du client à partir de son socket
                client_id = client_sockets[s]
                print(f"Client {client_id} disconnected")
                sockets.remove(s)
                # Supprimer l'entrée du client du dictionnaire
                del client_sockets[s]
                s.close()
