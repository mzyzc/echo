# Analysis

## The problem

When talking to an individual or a group of people, humans naturally assume that the members present are the only ones aware of what is being said. Online, this is not always the case; malicious individuals are able to perform man-in-the-middle attacks and 'hear' everything being said or intercept the server managing the communications to possibly reveal messages to third parties.

With the growing importance of technology in our world, it is important that people are able to accomplish their tasks without a lingering fear that someone might be listening in. There are several means by which people can communicate online but most of them either don't implement end-to-end encryption or make it convenient for the user to take advantage of it.

### Current solutions

#### Unencrypted

- SMS

SMS is a basic set of protocols with no built-in support for encryption. An app called Silence offers the ability to send encrypted SMS messages between its users. Since SMS doesn't support rich text formatting, is carrier-dependent, and is also declining in use, I would like to use a less-restricting technology.

#### Encrypted but with some disadvantages

- iMessage: uses end-to-end encryption but can only be used between Apple devices
- Facebook Messenger: encrypted but feature not enabled by default
- Telegram: same Facebook Messenger
- Encrypted email: often difficult for the average user to set up

Some attempts at creating a secure messenger have been quite successful: iMessage achieves both the goals of being secure and simple to use but unfortunately is not usable by everyone due to the Apple device restriction.

Both Telegram and Facebook Messenger offer end-to-end encryption through a 'secret chat' feature. Unfortunately, these are not enabled by default so many users either won't know about their existence, what they do, or will simply forgo using them for convenience.

#### Encrypted and easy to use

- WhatsApp
- Signal

The Signal messenger developed its own cryptographic protocol in 2013 which has since been adopted by WhatsApp as well. Both of these apps encrypt data by default, making it simple for users to communicate securely.

Since both of these products fulfil my criteria for a good encrypted messenger, my program simply aims to be an alternative.

### My proposed solution

I intend to develop a new messaging app that will make sending messages between users as frictionless as possible. These are the criteria that it must achieve:

- Messages must be end-to-end encrypted
- Encryption must be enabled by default
- Sending an encrypted message should require minimal technical knowledge
- Sending an encrypted message should require minimal effort

## The user

Although the goals of this program will likely appeal to a broad audience, it is specifically aimed at non-technical users who wouldn't otherwise know how to send messages securely. I believe that other potentially interested parties like power users and organisations likely already have the knowledge and resources available to achieve these goals by other means.

The application will contain some features catered towards more advanced users (should they wish to use them) but the primary focus will be to make the experience as simple as possible for a new user.

### The interview

**What is your primary method of communicating with others online?**
...

**What other methods do you use or have used in the past?**
...

**Have you ever sent messages or media that you would like to remain private?**
...

**Have you ever felt worries about a third party seeing your messages?**
...

**Have you ever taken any steps to make your communications safer or more secure?**
...

**If so, describe your experience.**
...
