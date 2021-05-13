# Testing

I've made unit tests to verify correct server functionality. It can correctly authenticate users, input into and output from the database, and safely handle errors without crashing.

A video demo of the client application being used is shown below. It demonstrates a user registering, logging in, creating a conversation with multiple users, and sending messages within that conversation. Refresh functionality is available to view new messages and conversations without restarting the app.

![Demo of the client in use](../assets/echo.mp4)

The client has been tested to work on Android and Linux devices. It is likely to work on iOS and Windows too due to Flutter's cross-platform capabilities. A web version is partially functional but it cannot get past the login screen due to network issues; browsers cannot use normal system TCP sockets so Echo would either need to be modified to use WebSockets or compiled to WebAssembly. Neither of these options are currently implemented but they could reasonably be done in the future.

The server has been running for around a month with moderately frequent activity and has not been observed to crash or mismanage data in any way.

## Debugging client

Developing a server and a client side-by-side meant that one would often have support for a feature before the other, making it difficult to test things. My solution to this was to make a second, lightweight client that can be run on the command line.

This project is called `echo-cli`, and it was useful for testing server functionality before the main client caught up in features. Being a debugging tool, it is not ideal for day-to-day use but it helped speed development up.

I would use this client to send and retrieve messages as raw requests. This allowed me to not get caught up in the design of the app and directly verify whether a server response looks as expected.
