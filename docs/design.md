# Design

## Design decisions

One objective for this program is to be cross-platform. As implementing a native client for each platform would require a lot of work and duplicated effort, I have chosen to use a UI toolkit called Flutter to create iOS, Android, and web apps.

A centralised server will be used to make management easier and allow communication to occur in a platform-agnostic way.

![Client-server architecture](../assets/client-server.png)

The server will be written in the Rust programming language due to its strict memory checking features, good performance, and multithreading support. I believe these properties complement the server's role well since speed and reliability is crucial here. The client will be written in Dart because this is the language used by the Flutter toolkit. When the program is compiled, the Dart code will be converted to each platform's native language (Java/Kotlin for Android, Swift for iOS, and JavaScript for the web).

At the core of the system lies the asymmetric method of encryption. Each user will generate a pair of keys: one for encrypting messages (the public key) and one for decrypting them (the private key). This system makes cracking very difficult but can be slow due to its complexity.

The specific algorithms I will use are x25519 for exchange and ed25519 for signing. These both come from the elliptic-curve family of algorithms which, compared to Rivest-Shamir-Adleman (RSA), are fast at converting data and use very small key sizes for the same degree of security. This is significant because my application will largely be used on mobile phones which may not have powerful hardware. My reason for choosing these two over other elliptic-curve algorithms is that they are implemented in almost all languages.

![Generating a key pair](../assets/key-pair.png)

To solve the speed problem, I will use a separate 'session key' to encrypt and decrypt individual messages. Since it is obtained via the key pairs, it inherits a lot of the benefits of asymmetric cryptography while being much faster and less computationally-expensive.

Instead of generating a completely new key and sharing it between users, I am instead creating it from the recipient's private key and the sender's public key. The benefit of this is not having to pass the key across a network, reducing overhead and making it immune to man-in-the-middle interception.

![Encrypting a message with a session key](../assets/encrypt-message.png)

As an extra layer of security against man-in-the-middle attacks, the program verifies the sender of each message using a digital signature. This is created by encrypting the digest (hashed version of message) with the sender's private key and sending it along with the message.

![Creating a signature](../assets/create-sig.png)

Once the user receives the message, they can create their own hash and compare it to the decrypted form of the digest they received (using the sender's public key).

![Verifying a signature](../assets/verify-sig.png)

When the client initialises, it will create a persistent TCP connection with the server that will stay open until the app is closed. I chose this approach because of its simplicity; the server does not have to keep track of who connects to it or initiate connections with them.

Clients will encode messages in JSON form (due to its ubiquity as a data exchange format) and send them over a secure TLS connection. The server has no knowledge of the precise contents of the messages it receives and will only move them in and out of the database. This keeps the data secure even if the server was to be compromised.

On the server, a TCP listener is bound to port 63100 (not used in any major software). It accepts incoming connections asynchronously (to maximise performance) and continuously polls the client (every 500 ms) to maintain a connection. Echo connects to a PostgreSQL database upon initialising and will read or write data to it based on the client's requests.

## Process

### Client logic

#### Sending

1. Exchange key pairs
    1. User1 generates a key pair
    2. User2 generates a key pair
    3. User1 sends their public key to User2
    4. User2 sends their public key to User1
2. Establish a session key
    1. Local private key combined with remote public key to create session key
3. Compose message
4. Encrypt the message
    1. User1 writes a message
    2. Create a signature
        1. Message contents are hashed to produce a digest
        2. User1 encrypts the digest using their private key
    3. Message encrypted using the session key
    4. Encrypted message and digest are bundled together
5. Transmit message to server

#### Receiving

1. Receive message
    1. User2 decrypts message using the session key
2. Verify signature
    1. User2 decrypts digest using User1's public key to produce first digest
    2. Message contents hashed to produce the second digest
    3. Check if digests match
3. Display message
    1. If signature could not be verified, display a warning to the user

### Server logic

1. Receive message
2. Interpret client request
  - If registering, add user information to database
  - If receiving a message, add it to database and relay it to user
3. Transmit message to User2

## Classes

![Class diagram](../assets/classes.png)

Since I want the program to support images and video in addition to plaintext, a `media_type` must be specified for each message in the standard MIME format so that clients know how to interpret the data.

## Database structure

![Entity relationship diagram](../assets/erd.png)

- Users
    - **UserID**
    - PublicKey
    - DisplayName
- Messages
    - **MessageID**
    - Data
    - MediaType
    - Timestamp
    - Signature
    - Conversation: Conversations[ConversationID]
- Conversations
    - **ConversationID**
    - Sender: Users[UserID]
    - Receipient: Users[UserID]

## Functions

### Client

```
Keyring.genKeys()
Keyring.createExchangePair() -> exchangeKeyPair
Keyring.createSigningPair(localPrivateKey, remotePublicKey) -> signingKeyPair
Keyring.createSessionKey(localPrivateKey, remotePublicKey) -> sessionKey
Keyring.import()
Keyring.export()

Message.initialize(data, mediaType, sessionKey, signingKeyPair)
Message.convert(data, sessionKey) -> data
Message.sign(privateKey) -> signature
Message.verifySignature(signingKeyPair) -> bool
Message.send()

DataSocket.initialize(hostname)
```

### Server

```
handle_client(TcpStream)
```
