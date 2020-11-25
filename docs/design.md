# Message structure

```
message_object:
    message_text: string
    sender_ip: int[]
    receipient_ip: int[]
    date_sent: dateTime
    isHashed: bool
```

# Process

`[User1] <--> {Server} <--> [User2]`

Note that User1 and User2 are equivalent; the distinction is only made for clarity and consistency in the explanations

`[Function] --> [Public Key]+[Private Key]`

`[Session Key]+[Message] --> [Function] --> [Hashed Message]`

1. Exchange key pairs
    1. User1 generates a key pair
    2. User2 generates a key pair
    3. User1 sends their public key to User2 via plaintext
    4. User2 sends their public key to User1 via plaintext
    5. User1 generates a symmetric key and encrypts it with User2's public key
    6. User1 sends the encrypted symmetric key to User2
    7. User2 decrypts the encrypted symmetric key
2. Establish a session key
    1. User1 generates a symmetric key and encrypts it with User2's public key
    2. User1 sends the encrypted symmetric key to User2
    3. User2 decrypts the encrypted symmetric key
3. Compose message
    1. User1 writes a message
    2. User1 encrypts the message using the symmetric key
    3. User1 sends the message
4. Transmit message
    1. Transmit message to server
    2. Add message to database
    3. Transmit message to User2
5. Receive message
    1. User2 receives message
    2. User2 decrypts message using the symmetric key
    2. Message displayed on User2 client

# Database structure

- Users
    - ID
    - Forename
    - Surname
- Messages
    - ID
    - DataHash
    - MediaType
    - Timestamp
    - Sender[Users]
    - Receipient[Users]

# Functions

```
generateKeyPair() -> (publicKey, privateKey)
generateSessionKey() -> sessionKey
encryptSessionKey(sessionKey, publicKey) -> sessionKey
decryptSessionKey(sessionKey, privateKey) -> sessionKey
buildMessage(data, media_type) -> message_object
sendMessage(message_object, (dest_ip, dest_port))
encryptMessage(message_object) -> message_object
decryptMessage(message_object) -> message_object
```

# Explanations

I chose to use a 'session key' to encrypt and decrypt individual messages instead of using the key pairs directly. This lowers the latency between sending and receiving messages while still providing the benefits of asymmetric encryption when sharing the symmetric key.
