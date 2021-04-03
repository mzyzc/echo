# Design

## Dependencies

The following libraries were used for features too complex, tedious, or irrelevant to implement myself. Since security is a major goal of this project, I have chosen to use professional and well-tested cryptographic algorithms instead of creating my own (likely insecure) versions.

One of the objectives for this project is to be cross-platform. It is not feasible to create a native client for every individual platform due to time constraints and duplication of effort. As an alternative, I have chosen a UI toolkit called Flutter which I can use to create native applications for iOS, Android, and the web.

### Server

- **argon2** to hash user passwords
- **async-std** to allow code to run asynchronously
- **async-tls** and **rustls** to establish secure TLS connections
- **base64** to decode binary data
- **dotenv** to simplify configuring the application
- **env-logger** and **log** for more informative logging
- **getrandom** for generating random data
- **sqlx** for interacting with a database
- **serde** for converting data to and from JSON

### Client

- **flutter** for building the GUI
- **cryptography-flutter** for encrypting data across multiple platforms
- **path-provider** to access the filesystem

## Interface

![Login screen](../assets/ui-login.jpg)

The login screen is simple and doesn't immediately ask for much information. This should help new users get started quickly.

![Conversations screen](../assets/ui-conversations.jpg)

Three elements make up the conversations screen: a header bar, a list of conversations, and a navigation bar at the bottom. The navigation bar was positioned at the bottom because that is the location closest to the thumb, aiding ergonomics.

At the bottom of the list is a small button with a plus symbol on it which is used to start new conversations. This is a fairly traditional UI so it should be familiar to users.

![Messages screen](../assets/ui-messages.jpg)

Each conversation has a messages page with its name on the header bar to help the user keep track of who they are talking to. The bottom of the page has a persistent message box so that participants can start writing at any point in the conversation.

Yet again, this is a common design and users will likely immediately know what to do.

## Architecture

A centralised server will be used to simplify data management and allow communications to happen easily regardless of the specific client.

![Client-server architecture](../assets/client-server.png)

The server will be written in the Rust programming language due to its strict memory checking features, good performance, and multithreading support. I believe these properties complement the server's role well since speed and reliability is crucial for such a component. The client will be written in Dart because this is the language used by the Flutter toolkit. When the program is compiled, this code will be converted to each platform's native language (Java/Kotlin for Android, Swift for iOS, and JavaScript for the web).

## Operation

When the client initialises, it creates a persistent TLS connection with the server which will stay open until the app is closed. This simplifies communication because the server does not have to keep track of who connects to it or initiates connections with it; clients simply request the information they need through the existing connection without any additional authentication necessary.

On the server, a TCP listener is bound to port 63100 (not used in any major software). It accepts incoming connections asynchronously and continuously polls the client (every 500 ms, by default) in order to maintain a connection and acknowledge requests. Upon initialisation, it connects to a PostgreSQL database and accesses it according to the client's requests.

Data sent over the network follows a custom JSON-based protocol which specifies a function along with necessary operands:

```
{
  'function': 'CREATE USER',
  'users': [{
    'email': 'john@example.com',
    'password': 'p@$$w0rd',
    'publicKey': 'VGhlIEVjaG8gc2VjdXJlIG1lc3Nlbmdlcg=='
  }]
}
```

The function is made up of an operation and a target. All the operations (excluding VERIFY) correspond to a CRUD action (CREATE, READ, UPDATE, DELETE). Possible targets include USER, CONVERSATION, and MESSAGE.

JSON was chosen because of its ubiquity as a data exchange format. Base64 is used to encode binary data because it is more concise than a byte array (less data to transfer over the network) and consists only of ASCII characters.

## Process

### Client

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

### Server

1. Receive message
2. Interpret client request
  - If registering, add user information to database
  - If receiving a message, add it to database and relay it to user
3. Transmit message to User2

## Security

Most data (including messages) is encrypted before being sent to the server. This means the server has no precise knowledge of what it receives and stores it in scrambled form. As a result, the client is the only one who ever sees the plaintext version; no sensitive data is ever transferred over the network or stored in the database. The exception to this is public information which doesn't benefit from encryption and certain metadata which is useful for the server to correctly identity the information it manages. For example, public keys or the members present in a conversation.

Since the server's API is public, anyone can, in theory, create their own client for this program. As a result, it cannot be assumed that passwords have been hashed prior to transmission and hence this is done on the server. To retain security, the exchange of data happens over a secure TLS connection which keeps passwords safe in transmission and adds an additional layer of protection against man-in-the-middle attacks.

### Asymmetric encryption

At the core of the system lies the asymmetric method of encryption. Each user will generate a pair of keys: one for encrypting messages (the public key) and one for decrypting them (the private key). This system makes cracking very difficult but can be slow due to its complexity. The private key will be kept locally on the user's device while the public key will simply be stored on the remote database.

![Generating a key pair](../assets/key-pair.png)

The specific algorithm I will be using is X25519. This is an elliptic-curve-based algorithm which, compared to Rivest-Shamir-Adleman (RSA), is fast at converting data and uses very small key sizes for the same degree of security. This is significant because my application will largely be used on mobile phones which may not have powerful hardware. The reason I chose this over other forms of elliptic-curve cryptography is that it is implemented in almost all languages, making it easier to implement new clients in the future if required.

### Symmetric encryption

To solve the speed problem, I will use an independent 'session key' to encrypt and decrypt individual messages. It is derived from the key pairs, hence it inherits a lot of the benefits of asymmetric cryptography while being much faster and less computationally-expensive.

The session key is derived from the recipient's private key and the sender's public key. The benefit of this approach is that the key does not need to be passed over a network, reducing transmission overhead and making it completely immune to man-in-the-middle interception.

![Encrypting a message with a session key](../assets/encrypt-message.png)

#### X25519

X25519 is a 128-bit Diffie-Hellman function based on the Curve25519 elliptic curve.

Being a Diffie-Hellman function, X25519 exchanges keys asymmetrically. Each member of the exchange generates a private key and a public key, but both can combine their private key with the other's public key and obtain the same result: a shared secret. This shared secret, once established, can be used a key for ordinary symmetric encryption.

1. Each user starts with a 32-byte private key.
2. A corresponding 32-byte public key is created by passing the private key and public string 9 into a Curve25519 function.
3. Shared secret can be computed by combining one user's public key with another user's private key.

Mathematically, Curve25519 uses the Montgomery curve `y^2 = x^3 + 486662x^2 + x` over the prime field defined by the prime number `2^255 - 19`. Montgomery curves are a type of elliptic curve, and they all have an equivalent twisted Edwards curve; in the case of X25519, the Edwards curve is Ed25519 and is used for signatures.

### Signatures

As an extra layer of security against man-in-the-middle attacks, the program verifies the sender of each message using a digital signature. This is created by encrypting the digest (hashed version of message) with the sender's private key and sending it along with the message.

![Creating a signature](../assets/create-sig.png)

Once the user receives the message, they can create their own hash and compare it to the decrypted form of the digest they received (using the sender's public key).

![Verifying a signature](../assets/verify-sig.png)

I will use the Ed25519 algorithm for signing. This is another elliptic-curve-based algorithm which serves as a counterpart to X25519 and was chosen for the same reasons.

#### Ed25519

Ed25519 is the birationally equivalent twisted Edwards curve for Curve25519. Since the two are linked, Ed25519 is used to create signatures for secrets made with X25519.

A nonce (number used once) is a secret value used for every signature to keep the private key unknown.

## API

### VERIFY USERS

Verifies a user for the current connection. Almost all requests require this to be run first. Unlike most other functions, only one user can be specified here.

#### Request

- user
    - email
    - password

#### Response

- success

### CREATE USERS

Adds user data to the database. Users don't need to be verified to run this.

#### Request

- user
    - email
    - password
    - publicKey

#### Response

- success

### CREATE CONVERSATIONS

Creates a single conversation including the specified users.

#### Request

- conversation
    - name
- users
    - email

#### Response

- success

### CREATE MESSAGES

Adds messages to a conversation.

#### Request

- messages
    - data
    - mediaType
    - timestamp
    - signature
- conversation
    - id

#### Response

- success

### READ CONVERSATIONS

Lists all the conversations the user is a part of.

#### Request

#### Response

- conversations
    - conversationId
    - conversationName

### READ MESSAGES

Lists all the messages in a conversation.

#### Request

- conversationId

#### Response

- messages
    - user
        - id
        - displayName
    - data
    - mediaType
    - timestamp
    - signature

### READ USERS

Lists all the users that are part of a conversation.

#### Request

- conversationId

#### Response

- id
- email
- displayName
- publicKey

## Classes

![Class diagram](../assets/classes.png)

Since I want the program to support arbitrary data formats (like images or video) and not only plaintext, a `media_type` is specified for each message. This is formatted in standard MIME format so that clients are able to properly interpret the data.

## Database structure

![Entity relationship diagram](../assets/erd.png)

A `participant` is an identity of a user that is specific to a certain conversation.

- Users
    - **ID**
    - Email
    - PublicKey
    - Password
    - Salt
- Messages
    - **ID**
    - Data
    - MediaType
    - Timestamp
    - Signature
    - Sender: Participants[ID]
- Participants
    - **ID**
    - Name
    - Identity: Users[ID]
    - Conversation: Conversations[ID]
- Conversations
    - **ID**
    - Timestamp

## Functions

### Client

```
Keyring.genKeys()
Keyring.createExchangePair() -> exchangeKeyPair
Keyring.createSigningPair(localPrivateKey, remotePublicKey) -> signingKeyPair
Keyring.createSessionKey(localPrivateKey, remotePublicKey) -> sessionKey
Keyring.import()
Keyring.export()

Conversation.fromJson(json) -> Conversation

Message.fromJson(json) -> Message
Message.compose(data, mediaType) -> Message
Message.fetch(conversationId) -> List<Message>
Message.convert(data, sessionKey) -> data
Message.sign(privateKey) -> signature
Message.verifySignature(signingKeyPair) -> bool
Message.send()

User.fromJson(json) -> User
User.register()
User.login()

Server.connect(hostname)
Server.write(data)
Server.listen() -> List<int>
```

### Server

```
handle_connection(stream, tlsAcceptor, dbPool)
handle_request(data, dbPool, user)
format_response(response) -> String
init_db() -> dbPool

User.from_json(data)
Message.from_json(data)
Conversation.from_json(data)

Request.from_json(data)
Request.verify_users(login, dbPool) -> Response
Request.create_users(login, dbPool) -> Response
Request.create_conversations(login, dbPool) -> Response
Request.create_messages(login, dbPool) -> Response
Request.read_conversations(login, dbPool) -> Response
Request.read_messages(login, dbPool) -> Response
Request.read_users(login, dbPool) -> Response

Response.to_json() -> String
Response.users_to_json() -> String
Response.messages_to_json() -> String
Response.conversations_to_json() -> String

Tls.get_acceptor() -> tlsAcceptor
Tls.get_cert(path) -> certificate
Tls.get_key(path) -> privateKey

Login.authenticate(email)

Password.hash(password, salt) -> password
Password.is_valid(password) -> bool

Settings.is_enabled() -> bool
```
