# Evaluation

## Did the project achieve its goals?

Overall, the project was on an excellent trajectory to achieving its goal of providing a secure and easy-to-use messenger.

The app is both easy to use and makes use of strong encryption techniques. However, decryption is only partially implemented. As a result, all received messages appear to be garbled to the user.

### Capabilities and ease of use

As far as enabling users to send end-to-end encrypted messages easily and securely, the project has been a resounding success. Correct behaviour has been verified for both the server and the client programs.

The client is capable of encrypting, decrypting, signing, and validating the signatures of a foreign message---not held back by any technical barriers. All the encryption details have been hidden from the user, offering an uncomplicated experience. The server responds quickly so latency between sending an receiving a message is low.

### Platform support

The project's goal of being multi-platform is not currently achieved due to two major reasons: Flutter applications on the web and the desktop are currently either in beta or under active development, meaning they could definitely exist in the future once those platforms are supported. Secondly, the browser cannot interact with system sockets directly so the web version of the client is able to *run,* but not interact with the server. Both of these issues are fixable either through time or some additional development.

The project's' goal of being multi-platform has also been achieved. Both the Android and Linux versions of the app have been tested to work and this likely extends to iOS and Windows as well, at the least. This is enough platform coverage for most people to be able to access it.

However, the desktop versions are offered to Flutter via a beta setting. This is most likely going to change without any changes from me as a developer, but it is worth noting for the moment.

### Additional features

As a bonus goal, Echo aimed to have some additional features to cater to users that desire more than a simple app. The feature set of Echo is quite limited so I do not believe this goal was achieved.

However, the alternative client used for debugging, `echo-cli`, could potentially serve this purpose. Despite Echo's protocol being simple, power users are able to conveniently create server requests and do things that the main client is currently unable to do.

Additionally, Echo was designed to be an open protocol. Those who want more advanced features could, in theory, create alternative clients to fulfil those needs. Since these types of users are more likely to be technically-apt, this would be a realistic possibility as Echo grows.

## Technical concerns

There is currently a singleton being used in the client application for communication with the server. Ideally, I would like to replace this with a solution which doesn't require using the global state but due to time constraints and convenience I have stuck with this solution.

## For the future

If I was going to develop this project again, I would do more research of the technologies I am using in advance. This would allow me to get to working faster without having to spend as much time learning about the theory of what I'm doing.

The program is missing many convenience features which users might expect in a modern messaging application. This was not a strict goal in the original analysis, but it would definitely be a consideration if the project was going to continue development or be rewritten.

## Appendix

Jack, the third party that this app was developed for, had some feedback to share regarding his experience with the app.

---

Overall, what are your thoughts on Echo?

> Well, I can't currently use it since all the messages are scrambled. Once that gets fixed, I might be able to say more. The design looks nice though!

How easy was it to create an account on Echo?

> Very easy; I just typed in my email and password and I had an account right away.

What devices did you use the app on and how was your experience on each?

> I have an Android phone and a Windows laptop that I installed Echo on. Both worked perfectly as far as navigating the app goes and I didn't encounter any errors. The Windows version looks a bit odd though; it definitely seems like something made for a phone.


