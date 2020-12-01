# Design

## Design decisions

One of the objectives for this program is that it must work on several platforms. Implementing a native client for all possible devices would require a lot of effort so I have decided that the program will only be accessible through both a native Android app and a web client. The system will be centralised so both clients are able to communicate with each other using the same server. This offers the advantage of both making it simple for users to communicate between platforms in a manageable way.

Because the server holds the very important role of managing every message sent between users, it is crucial that it manages data swiftly and with minimal errors. I will write it in the Rust programming language due to its strict memory checking features and high performance because I believe these properties complement its purpose very well. Native Android applications can either be written in Java or Kotlin; I've decided to use Java since this is a more familiar language to me and the latter offers no significant benefits for my project. The web client will use HTML and CSS for the user interface and JavaScript for the logic.

## Message structure

Messages will be stored as an object holding both the message contents and some additional metadata.

```
message_object:
    message_text: string
    media_type: string
    timestamp: dateTime
    sender_id: int
    signature: string
```

Since I want the program to support images and video in addition to plaintext, a `media_type` must be specified in the standard MIME format so that the clients know how to interpret the data.

## Process

![User1 and User2 communicating with a server](../assets/client-server.png)

Note that User1 and User2 are equivalent; the distinction is only made for clarity and consistency in the explanations

![A function generates a public and a private key](../assets/key-pair.png)

![A message and a session key are passed through a function to produce a hashed message](../assets/encrypt-message.png)

## Client logic

### Sending

1. Exchange key pairs
    1. User1 generates a key pair
    2. User2 generates a key pair
    3. User1 sends their public key to User2 via plaintext
    4. User2 sends their public key to User1 via plaintext
2. Establish a session key
    1. User1 generates a symmetric key and encrypts it with User2's public key
    2. User1 sends the encrypted symmetric key to User2
    3. User2 decrypts the encrypted symmetric key
    4. User1 and User2 both store the session key locally
3. Compose message
4. Encrypt the message
    1. User1 writes a message
    2. Create a signature
        1. Message contents are hashed to produce a digest
        2. User1 encrypts the digest using their private key
    3. Message encrypted using the session key
    4. Encrypted message and digest are bundled together
5. Transmit message to server

### Receiving

1. Receive message
    1. User2 decrypts message using the session key
2. Verify signature
    1. User2 decrypts digest using User1's public key to produce first digest
    2. Message contents hashed to produce the second digest
    3. Check if digests match
3. Display message
    1. If signature could not be verified, display a warning to the user

## Server logic

1. Receive message
2. Check if user present in database
    1. If yes, move onto the next step
    1. If no, add their information and public key
3. Add message to database
4. Transmit message to User2

## Database structure

- Users
    - UserID
    - PublicKey
    - Forename
    - Surname
- Messages
    - MessageID
    - MessageHash
    - MediaType
    - Timestamp
    - Signature
    - Sender: Users[UserID]
    - Receipient: Users[UserID]

## Functions

```
generateKeyPair() -> (publicKey, privateKey)
generateSessionKey() -> sessionKey
encryptSessionKey(sessionKey, publicKey) -> sessionKey
decryptSessionKey(sessionKey, privateKey) -> sessionKey
buildMessage(data, media_type) -> message_object
sendMessage(message_object, destination)
encryptMessage(message_object, sessionKey) -> message_object
decryptMessage(message_object, sessionKey) -> message_object
```

## Explanations

I chose to use a 'session key' to encrypt and decrypt individual messages instead of using the key pairs directly because asymmetric encryption is relatively slow. This lowers the latency between sending and receiving messages while still providing the benefits of asymmetric encryption while the symmetric key is being shared.
