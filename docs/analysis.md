# Analysis

## The problem

When talking to an individual or a group of people, humans naturally assume that the members present are the only ones aware of what is being said. Online, this is not always the case; malicious individuals are able to perform man-in-the-middle attacks and 'hear' everything being said or intercept the server managing the communications to possibly reveal messages to third parties.

With the growing importance of technology in our world, it is important that people are able to accomplish their tasks without a lingering fear that someone might be listening in. There are several means by which people can communicate online but most of them either don't implement end-to-end encryption or don't make it convenient for the user to take advantage of it.

### Current solutions

#### Unencrypted

- SMS

SMS is a basic set of protocols with no built-in support for encryption and many disadvantages: it does not support rich text formatting, is carrier-dependent, is designed to only support very short messages, and is declining in usage. All of these things considered, I believe using such a restrictive technology as a serious means of secure communication would be a mistake as users are likely to become frustrated and miss the convenience and additional features offered by other applications.

An app called Silence offers the ability to send encrypted SMS messages between its users at a level of security similar to other encrypted messengers. It does not require an internet connection but this comes at the cost of depending on the carrier. Although the implementation of the program is good, the underlying limitations of SMS listed above make this solution a poor fit for many situations.

#### Encrypted but with some disadvantages

- iMessage: uses end-to-end encryption but can only be used between Apple devices
- Facebook Messenger: encrypted but feature not enabled by default
- Telegram: same Facebook Messenger
- Encrypted email: often difficult for the average user to set up

Some attempts at creating a secure messenger have been quite successful: iMessage achieves both the goals of being secure and simple to use but unfortunately is not usable by everyone due to the Apple device restriction.  However, it does deserve praise for making encrypted messaging very painless for its users; you need no knowledge of what encryption is or how it works to be able to use it.

Both Telegram and Facebook Messenger offer end-to-end encryption through a 'secret chat' feature. Unfortunately, these are not enabled by default so many users either won't know about their existence, what they do, or will simply forgo using them for convenience.

Email is not an encrypted system by design but asymmetric encryption is often used to fill this purpose through PGP. This approach has seen moderate success with its main limiting factor being difficulty to use: users must generate a key pair and manually distribute public keys with people they want to talk to. If the user does not understand how the system works, they can accidentally share the wrong key and not only nullify the whole process but also frustrate themselves. As a result, PGP encryption is mostly utilised by technical users and carries a high barrier for entry for others. Some clients and email providers can simplify the process but it is far from universally accessible.

#### Encrypted and easy to use

- WhatsApp
- Signal

The Signal protocol is perhaps the industry standard for secure messaging; it is used by both WhatsApp and Signal (the app for which it was made). In addition to using a mixture of cryptographically secure algorithms, it also offers perfect forward secrecy which means that, if a secret key is compromised at any point in time, all past conversations will remain confidential.

Both apps are simple to use and require no knowledge of computer encryption to send a simple message. Since both fulfil my criteria for a good encrypted messenger, my program simply aims to be an alternative.

## The user

Although the goals of this program will likely appeal to a broad audience, it is specifically aimed at non-technical users who wouldn't otherwise know how to send messages securely. I believe that other potentially interested parties like power users and organisations likely already have the knowledge and resources available to achieve these goals by other means.

The application will contain some features catered towards more advanced users (should they wish to use them) but the primary focus will be to make the experience as simple as possible for a new user.

### The interview

**What is your primary method of communicating with others online?**

I use different apps depending on the person I'm talking to. I think Facebook Messenger is probably the main one.

**What other methods do you use or have used in the past?**

Social media, WhatsApp, SMS (when I need to)

**Have you ever sent messages or media that you would like to remain private?**

Yes, of course.

**Have you ever felt worried about a third party seeing your messages?**

Sometimes. Depends on what I'm messaging about.

**Have you ever taken any steps to make your communications safer or more secure?**

I've considered it a few times but things either seem too complicated or not something most people I know would be interested in.

**If so, describe your experience.**

I've tried using the 'secret chat' feature in Facebook Messenger before but it's really annoying to have to switch back and forth.

### My proposed solution

I intend to develop a new messaging app that will make sending messages between users as frictionless as possible. These are the criteria that it must achieve:

- Messages must be end-to-end encrypted
- Encryption must be enabled by default
- Sending an encrypted message should require minimal technical knowledge
- Sending an encrypted message should require minimal effort
- Be usable on all major platforms (iOS, Android, Windows, macOS, Linux)

During the interview, the user stated that they sometimes wanted their messages to remain secret but the people they communicate with wouldn't be interested. The obvious solution to this is encryption but since switching between encrypted and unencrypted messaging in the middle of a conversation can be cumbersome, it makes the most sense to enable it by default; the user will be able to take advantage of it without having to actively consider enabling it. Likewise, their peers, who may not care as much about secrecy, won't have to put in effort to cooperate.

One of the major problems the user expressed is secure messaging being "difficult". Addressing this issue is important because privacy is not usually a priority for users but rather something that they desire on occasion. As a result, users can easily give up on it when the process requires too much effort. A good encrypted messenger should make this simple so that the users determination does not run out before they are able to find a solution.

Since the program is used for communications, it should aim to maximise the amount of people that are able to access it. The solution to this is to make the app cross-platform so that it is accessible to nearly anyone. Mobile operating systems are a priority due to the nature of the program but many other apps offer a desktop client or web interface as well.

Unfortunately, making an app directly for iOS would be difficult since Apple's requirements for publishing an application to the App Store are very high and they offer no simple way to sideload programs. Hence, I will likely create a web interface for my app to get around this issue.
