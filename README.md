# P2P-PrivateMessaging
Peer-to-Peer Application to send secure messages

- This service employs a 'Registration' Server, where users can register their username, a public key and IP address.
- In order to connect with another user
  - The sender can use the Recipient's username to find their public key on the registration server
  - The sender can then use the key to encrypt a message, either with an IP or short direct message
  - The recipient can then access the encrypted message, and decrypt with their private Key
  - The recipient can then respond in kind.
  - Once both users have the public key of the other and their IP, they can communicate via sockets with asymmetrically encrypted messages.
