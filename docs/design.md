# Design

## Design decisions

One objective for this program is working on several platforms. Implementing a native client for every platform individually would require a lot of work and duplicated effort so I have decided to use a cross-platform toolkit called Flutter to create an iOS, Android, and web app.

A centralised server will be used for the system so that clients are able to communicate with each other using the same server. It offers the advantage of making the system easier to manage and allows communication to occur in a platform-agnostic way.

![Client-server architecture](../assets/client-server.png)

Because the server holds the very important role of managing every message sent between users, it is crucial that it manages data swiftly and with minimal errors. I will write it in the Rust programming language due to its strict memory checking features and high performance because I believe these properties complement its purpose very well. Native Android applications can either be written in Java or Kotlin; I've decided to use Java since this is a more familiar language to me and the latter offers no significant benefits for my project. The web client will use HTML and CSS for the user interface and JavaScript for the logic.

The server will be written in the Rust programming language due to its strict memory checking features, high performance, and multithreading support. I believe these properties complement the server's important role as something that manages data swiftly and with minimal errors. My clients will all be written in Dart as this is the language used by the Flutter toolkit; the final Dart code will be compiled to each platforms native application language (Java/Kotlin for Android, Swift for iOS, and JavaScript for the web).

At the heart of the system lies the asymmetric system of cryptography. Each user generates a pair of keys: one for encrypting messages (the public key) and one for decrypting them (the private key). This system makes cracking very difficult but it can be quite slow due to its complexity.

At the core of the system lies the asymmetric method of encryption. Each user will generate a pair of keys: one for encrypting messages (the public key) and one for decrypting them (the private key). This system makes cracking very difficult but can be slow due to its complexity.

The specific algorithm I will be using is ed25519, a member of the elliptic-curve cryptography family of algorithms. After comparing elliptic-curve-based algorithms (ECC) with Rivest-Shamir-Adleman (RSA), I have concluded that ECC is significantly faster at encrypting and decrypting data and uses much smaller key sizes for the same degree of security. This is important because my application will be used largely on mobile phones or possibly other low-power devices. My reason for choosing ed25519 specifically is its signature support, wide availability across platforms, and the fact that, unlike NIST-approved elliptic curves, it is not suspected of possessing a backdoor.

![Generating a key pair](../assets/key-pair.png)

To solve this problem, I will use a separate 'session key' to encrypt and decrypt individual messages instead of using the key pairs directly. This key will be shared via asymmetric encryption, so the increased security from that system will still apply while the session key offers decreased latency.

![Encrypting a message with a session key](../assets/encrypt-message.png)

To provide an extra layer of security against man-in-the-middle attacks, the program verifies the sender of each message using a digital signature. This is created by encrypting the digest (hashed version of message) with the sender's private key and sending it along with the message.

![Creating a signature](../assets/create-sig.png)

Once the user receives the message, they can create their own digest and compare it to the decrypted form of the digest they received (using the sender's public key).

![Verifying a signature](../assets/verify-sig.png)

Messages will be sent in JSON form (due to its conciseness and ubiquity as a data exchange format) over a secure TLS connection. The server will have no knowledge of what the contents of the messages it receives are and will store them in a database in hashed form so that information can remain safe even if the server is compromised.

## Process

### Client logic

#### Sending

1. Exchange key pairs
    1. User1 generates a key pair
    2. User2 generates a key pair
    3. User1 sends their public key to User2
    4. User2 sends their public key to User1
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
2. Check if user present in database
    1. If yes, move onto the next step
    1. If no, add their information and public key
3. Add message to database
4. Transmit message to User2

## Classes

![Class diagram](../assets/classes.png)

Since I want the program to support images and video in addition to plaintext, a `media_type` must be specified for each message in the standard MIME format so that clients know how to interpret the data.

## Database structure

![Entity relationship diagram](../assets/erd.png)

- Users
    * UserID
    - PublicKey
    - Forename
    - Surname
- Participant
    * ParticipantID
    - UserID: Users[UserID]
    - Nickname: Users[UserID]
- Messages
    * MessageID
    - MessageHash
    - MediaType
    - Timestamp
    - Signature
- Conversations
    * ConversationID
    - Sender: Participants[ParticipantID]
    - Receipient: Participants[ParticipantID]
    - MessageID

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
