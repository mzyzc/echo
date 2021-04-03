# Testing

I'm currently in the process of writing unit tests for all of my server functionality. Until then, I can informally verify that all data can be input into the database, and *some* data can be read correctly from it.

A video demo of the client application being used is below. The server is not fully complete at this point so all of the data in it is still a placeholder. However, the client does send messages to the server for registering, logging in, and sending a message.

![Demo of the client in use](../assets/echo.mp4)

The client has been tested to work on Android devices and is likely to work on iOS too, although this could not be verified due to system restrictions. A web version is partially functional but would need to be programmed to use WebSockets instead of the system's normal TCP sockets. This is currently not implemented but could reasonably be done in the future.
