# Analysis

## The problem

When talking to an individual or a group of people, humans naturally assume that the members present are the only ones aware of what is being said. Online, this is not always the case; malicious individuals are able to perform man-in-the-middle attacks and 'hear' everything being said or intercept the server managing communication, possibly revealing those messages to other third parties.

With the growing importance of technology in our world, it is important that people are able to accomplish their tasks without a lingering fear that someone might be listening in. There are severals means by which people can communicate online but most of them either don't implement end-to-end encryption or make it inconvenient for the user to take advantage of.

### Current solutions

- SMS
- Email
- Instant messaging apps

#### The problem with them

**No encryption** is a cardinal sin:

- SMS is unencrypted
- Facebook Messenger is unencrypted

SMS is a basic protocol with no built-in support for encryption. An app called Silence offers the ability to send encrypted SMS messages between its users. Since use of SMS is generally declining in favor of non-carrier-dependent apps, I would like to avoid using this technology.

**Poorly-implemented encryption** is somewhat better:

- iMessage uses end-to-end encryption but only between Apple devices
- Facebook Messenger and Telegram support encryption but it is not used by default
- Encrypted email is difficult to set up for the average user

Some attempts at a secure messenger have been quite successful. iMessage achieves the goal of being secure and simple to use but unfortunately is only available on Apple devices, hugely reducing its reach.

Both Telegram and Facebook Messenger offer end-to-end encryption through 'secret chat' features. Unfortunately, these are not used by default and many users won't even know about their existence.

**Well-implemented encryption** is encouraged:

- WhatsApp and Signal both encrypt data by default

### My proposed solution

My proposed solution is Echo: a new messaging application that makes it nearly effortless for users to send encrypted messages between each other.

#### Improvements over the current solutions

- Encrypted
- Encryption is enabled by default
- Sending an encrypted message should take minimal knowledge and effort

## The user

Although the goals this program intends to solve are likely to appeal to a wide audience, it is specifically aimed at non-technical users who don't otherwise know how to send messages securely. This is because power users and organisations, for instance, likely already have the knowledge or resources available to achieve these goals by other means.

The application will contain some features catered towards more advanced users but the primary focus will be to make the experience as simple as possible for a new user.

### Interview

Interviewing a regular person who likes unintercepted messages

#### What is your primary way of communicating with others online?

#### Have you ever been worried about the privacy of your messages?
