# Evaluation

## Did the project achieve its goals?

Overall, the project was on the right track to achieving its goals but didn't manage to deliver a full product before the deadline.

As far as enabling users to send end-to-end encrypted messages easily and securely, the project was on track to being a resounding success. Since certain parts of the server are not yet complete, correct behaviour could not be verified directly. However, the client is perfectly capable of encrypting, decrypting, signing, and validating the signatures of a foreign message---no technical barriers are holding it back. All the details of encryption were hidden from the user, offering an uncomplicated experience.

The project's goal of being multi-platform is not currently achieved due to two major reasons: Flutter applications on the web and the desktop are currently either in beta or under active development, meaning they could definitely exist in the future once those platforms are supported. Secondly, the browser cannot interact with system sockets directly so the web version of the client is able to *run,* but not interact with the server. Both of these issues are fixable either through time or some additional development.

## Technical concerns

There is currently a singleton being used in the client application for communication with the server. Ideally, I would like to replace this with a solution which doesn't require using the global state but due to time constraints I have stuck with this solution.

## For the future

If I was going to develop this project again, I would do more research of the technologies I am using in advance. This would allow me to get to working faster without having to spend as much time learning about the theory of what I'm doing.
