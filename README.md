# P2P-PrivateMessaging
Peer-to-Peer Application to send secure messages

- This service employs a 'Registration' Server, where users can register their username, a public key and IP address.
- In order to connect with another user
  - The sender can use the Recipient's username to find their public key on the registration server
  - The sender can then use the key to encrypt a message, either with an IP or short direct message
  - The recipient can then access the encrypted message, and decrypt with their private Key
  - The recipient can then respond in kind.
  - Once both users have the public key of the other and their IP, they can communicate via sockets with asymmetrically encrypted messages.

## Setup and Running

### Generating a Private and Public Key
Use the following commands in a terminal window to generate a Private and Public key for use in encrypting and decrypting messages

* Generate a private key
```
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```
* Extract a public key from the private key
```
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

### Registering Your Username
*Important: The Registration Server is not currently live. This application can still be used if you obtain the recipient's IP and shared key directly from the user*

* Provide the following to information to register your username and make it possible for other users to search for your contact information:
  * Username (Must be unique. If already in use, you must select another one)
  * Content of Shared Public Key file
  * IP Address

### Requirements for Running Application
The following is needed in order to run the P2P application:
* The Destination User's Public Key File (Expecting file named 'public_key.pem')
  * The key file must be in the same directory as the application
* The Destination User's IP Address

### Running P2P Application
*Important: This program runs with Python3, if that is not set as your default, replace python with python3 in the below instruction*

To start the application, enter the following command from the same directory as the python script and the public key file.
```
python socket_p2p.py
```

The P2P Application starts in listening mode. In order to send a message, you must press Ctrl+c, where you will then be prompted for your message and your intended recipient's IP

After sending the message, the application returns to listening mode.
