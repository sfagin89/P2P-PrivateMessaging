# Socket P2P
# Author: Sara Fagin
# Date: 5/7/22
#
# This Application is meant for P2P Socket communication
# Users can send messages between eachother with the
# Recipient's IP.
#
# Current Functionality:
# - User Selects Client or Server mode
# - Server mode sets User's device to listening for incoming connections
# - Client mode has User's device send a message to specified IP
# - - User's in Client mode can repeatedly send messages until choosing 'no'
# - - If Recipient is not currently listening, Client mode device will ask
#     if user wishes to retry sending the message until server is listening or
#     User decides to exit loop.
#
# Planned Functionality:
# - If User is not actively sending a message in client mode, device is in
#   listening mode.
# - While in Server listening mode, user has ability to change to change to
#   client mode and send a message
#
# Ideas:
# - If server isn't listening or busy when client tries to send a message
#   device will store outgoing message and check each loop if server is available
#   until it is able to send the message.
# - - If Outgoing Message Queue is not empty, try to establish connection with server


import socket
from _thread import *
import threading
import keyboard

try:
    s_global = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

debug = 1

# Lock to facilitate multithreading
mutex = threading.Lock()

# Function to Bind a Socket Post as the Server and
# listen for connections
def socketServerStart():
    print("Starting Socket Server")

    # Reserving Port
    port = 3600

    # Binding to port
    global s_global
    s_global.bind(('', port))
    print ("socket bound to %s" %(port))

    # Put the socket into listening mode
    s_global.listen(5)
    print ("socket is listening")

# Function to Accept a Socket Connection as the Server and
# receive data from Client
def socketServerRun():

    # Establish Connection with client
    c, addr = s_global.accept()
    print ('\nGot connection from', addr )

    # Receive and Print Message to Console
    msg_in = c.recv(1024)
    print(msg_in.decode())

    # Close the connection with the client
    c.close()

def socketClientRun(recipient):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if debug:
            print("Socket Successfully Created")
    except socket.error as err:
        print("Socket Creation Failed with Error %s" %(err))

    # Port set for Node Communication Socket
    port = 3600

    try:
        host_ip = socket.gethostbyname(recipient)
    except socket.gaierror:

        # this means could not resolve the host
        print ("There was an error resolving the host")
        sys.exit()

    # connecting to the server
    while True:
        try:
            s.connect((host_ip, port))
            print ("The socket has successfully connected to Server Node")
            break
        except ConnectionRefusedError:
            print('Server Node does not currently appear to be listening on port', port)
            retry = input('Do you want to try to send your message again?(y/n): ')
            if retry == 'y':
                continue
            else:
                exit()

    s.send('This is a message sent by the Client Node'.encode())

if __name__ == '__main__':
    print("Running Main")

    socketMode = input("Run this Node in (S)erver or (C)lient mode?: ")
    if (socketMode == "S"):
        socketServerStart()
    if (socketMode == "C"):
        host_ip = input("Please enter recipient IP: ")

    try:
        while True:
            if (socketMode == "S"):
                socketServerRun()
            elif (socketMode == "C"):
                while True:
                    socketClientRun(host_ip)
                    cont = input('Do you want to sent another message?(y/n): ')
                    if cont == 'y':
                        continue
                    else:
                        exit()
            else:
                print("No Socket Mode Selected")

    except KeyboardInterrupt:
        print("\nExiting Application\n")
        pass
