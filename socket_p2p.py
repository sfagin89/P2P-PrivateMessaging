# Socket P2P
# Author: Sara Fagin
# Date: 5/7/22
#
# This Application is meant for P2P Socket communication
# Users can send messages between eachother with the
# Recipient's IP.
#
# Current Functionality:
# - Application starts in Server Listening Mode
# - A lock is set everyime the application checks if a message is being received
# - if no message is seen, the lock is released
# - If user pressed 'Ctrl+c' they are prompted to enter a message and IP to
#   send the message to.
# - If user is in the process of writing sending a message when another message is
#   received, the message comes in, then the user can continue typeing their message
# - If Recipient is not currently listening, Client mode device will ask
#   if user wishes to retry sending the message until server is listening or
#   User decides to exit loop. After which it returns to listening mode
#
# - Currently no graceful exit of the application
#
# Planned Functionality
# - Graceful Exit at all stages of application
# - Encryption Functionality
#   -
#
# Ideas:
# - If server isn't listening or busy when client tries to send a message
#   device will store outgoing message and check each loop if server is available
#   until it is able to send the message.
#   - If Outgoing Message Queue is not empty, try to establish connection with server


import socket
from _thread import *
import threading
import keyboard

s_global = 0
debug = 1
# Lock to facilitate multithreading
mutex = threading.Lock()

def createSocket():
    try:
        global s_global
        s_global = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))

def closeSocket():
    s_global.close()

# Function to Bind a Socket Post as the Server and
# listen for connections
def socketServerStart():
    print("Starting Socket Server")

    # Creating Socket
    createSocket()

    # Reserving Port
    port = 5300

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
    while True:
        msg_in = c.recv(1024)
        if not msg_in:
            print("Releasing Lock")
            mutex.release()
            break
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
    port = 5300

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
    mutex.release()

if __name__ == '__main__':
    print("Running Main")

    #socketMode = input("Run this Node in (S)erver or (C)lient mode?: ")
    #if (socketMode == "S"):
    #    socketServerStart()
    #if (socketMode == "C"):
    #    host_ip = input("Please enter recipient IP: ")

    #try:
    #    while True:
    #        if (socketMode == "S"):
    #            socketServerRun()
    #        elif (socketMode == "C"):
    #            while True:
    #                socketClientRun(host_ip)
    #                cont = input('Do you want to sent another message?(y/n): ')
    #                if cont == 'y':
    #                    continue
    #                else:
    #                    exit()
    #        else:
    #            print("No Socket Mode Selected")

    #except KeyboardInterrupt:
    #    print("\nExiting Application\n")
    #    pass

    print("Application Entering Listening Mode. To send a Message, press 'Ctrl+c'")
    socketServerStart()

    while True:
        try:
            print("Acquiring Mutex Lock")
            mutex.acquire()
            print("Starting new SocketServerRun Thread")
            start_new_thread(socketServerRun, ())
        except KeyboardInterrupt:
            msg_out = input("\nPlease enter your message: ")
            host_ip = input("Please enter recipient IP: ")
            start_new_thread(socketClientRun, (host_ip,))
