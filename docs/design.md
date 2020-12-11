# Design

## Overview

One of the objectives for this program is that it must work on several platforms. Implementing a native client for all possible devices would require a lot of effort so I have decided that the program will only be accessible through both a native Android app and a web client. The system will be centralised so both clients are able to communicate with each other using the same server. This offers the advantage of both making it simple for users to communicate between platforms in a manageable way.

When creating the program, I will be using a Raspberry Pi as the server and various devices as clients.

![Client-server architecture](../assets/client-server.png)

Because the server holds the very important role of managing every message sent between users, it is crucial that it manages data swiftly and with minimal errors. I will write it in the Rust programming language due to its strict memory checking features and high performance because I believe these properties complement its purpose very well. I have chosen to use the Flutter toolkit (with the Dart language) for the client because it allows the application to run on multiple platforms without needing to rewrite large parts of the program logic for each client.

Most processing will be done on the server to reduce duplication of effort when creating the clients and ensuring behaviour is consistent on all platforms. This will also make it easier to build new clients in the future if the need arises.

At the heart of the program lies the asymmetric system of cryptography. Each user generates a pair of keys: one for encrypting messages (the public key) and one for decrypting them (the private key). This system makes cracking very difficult but it can be quite slow due to its complexity.

There are two major asymmetric encryptions systems which I have considered: Rivest–Shamir–Adleman (RSA) and elliptic-curve cryptography (ECC). I have chosen to use the latter for a few reasons:

- Keys are shorter than equivalent RSA keys so encrypting and decrypting is faster
- Less processing power required (useful for avoiding battery drain on phones)


![Generating a key pair](../assets/key-pair.png)

To solve this problem, I have chosen to use a separate 'session key' to encrypt and decrypt individual messages instead of using the key pairs directly. If the session key is shared asymmetrically, the latency between sending and receiving messages is lowered while still providing the benefits of public-key cryptography.

![Encrypting a message with a session key](../assets/encrypt-message.png)

To provide an extra layer of security against man-in-the-middle attacks, the program verifies each message using a digital signature. This is created by encrypting the digest (hashed version of message) with the sender's private key and sending it along with the message.

![Creating a signature](../assets/create-sig.png)

 When the message arrives, the recipient will decrypt the message using the sender's public key and compare it to a digest they created themselves.

![Verifying a signature](../assets/verify-sig.png)

## Process

### Client logic

#### Sending

1. Generate key pairs
    1. If Alice already has a key, skip this step
    2. Alice generates a key pair
    3. Alice sends her identity and public key to server
1. Exchange key pairs
    1. Alice sends her public key to Bob via plaintext
    2. Bob sends his public key to Alice via plaintext
2. Establish a session key
    1. Alice generates a symmetric key and encrypts it with Bob's public key
    2. Alice sends the encrypted symmetric key to Bob
    3. Bob decrypts the encrypted symmetric key
    4. Alice and Bob both store the session key locally
3. Compose message
4. Encrypt the message
    1. Create a signature
        1. Message contents are hashed to produce a digest
        2. Alice encrypts the digest using her private key
    2. Message encrypted using the session key
    3. Encrypted message and digest are bundled together
5. Transmit message to server

#### Receiving

1. Receive message
    1. Bob decrypts message using the session key
2. Verify signature
    1. Bob decrypts digest using Alice's public key to produce first digest
    2. Message contents hashed to produce the second digest
    3. Digests are compared to check if they match
3. Display message
    1. If signature could not be verified, display a warning to Alice
    2. Display the message to Alice

### Server logic

#### Registering a user

1. Receive user details
2. Add details and public key to database
3. Inform user whether operation was successful

#### Receiving a message

1. Receive message
2. Add message to database
3. Transmit message to User2

## Classes

![Class diagram](../assets/classes.png)

Since I want the program to support images and video in addition to plaintext, a `media_type` must be specified for each message in the standard MIME format so that clients know how to interpret the data.

## Database structure

![Entity relationship diagram](../assets/erd.png)

- Users
    - UserID
    - PublicKey
    - Forename
    - Surname
- Messages
    - MessageID
    - Contents
    - MediaType
    - Timestamp
    - Signature
- Conversations
    - MessageID: Messages[MessageID]
    - SenderID: Users[UserID]
    - ReceipientID: Users[UserID]

## Functions

```
generateKeyPair() -> (publicKey, privateKey)
generateSessionKey() -> sessionKey
encryptSessionKey(sessionKey, publicKey) -> sessionKey
decryptSessionKey(sessionKey, privateKey) -> sessionKey
generateDigest(messageContents) --> digest
createSignature(digest, privateKey) --> signature
decodeSignature(signature, publicKey) --> digest
buildMessage(data, mediaType) -> message
sendMessage(message, destination)
encryptMessage(message, sessionKey) -> message
decryptMessage(message, sessionKey) -> message
```
