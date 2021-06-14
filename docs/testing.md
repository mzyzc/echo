# Testing

I've made unit tests to verify correct server functionality. It can correctly authenticate users, input into and output from the database, and safely handle errors without crashing. Below is the output of the testing command:

```
running 7 tests
test api::tests::test_conversation_from_json ... ok
test api::request::tests::test_request_from_json ... ok
test api::tests::test_user_from_json ... ok
test api::tests::test_message_from_json ... ok
test settings::tests::test_is_enabled ... ok
test auth::tests::test_is_valid ... ok
test auth::tests::test_hash ... ok

test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.59s
```

All tests have passed and the program works as intended. The tests themselves can be viewed as part of their respective modules in the implementation section of the document.

## Video demonstration

A video demo of the client application being used is shown below. It demonstrates a user registering, logging in, creating a conversation with multiple users, and sending messages within that conversation. Refresh functionality is available to view new messages and conversations without restarting the app.

![Demo of the client in use](https://czyz.xyz/echo.mp4)

- At 00:11, the user tries to use an invalid email address. This is rejected and the user receives a notice.
- At 00:18, the user tries to login without entering a password. This is rejected and the user receives a notice.
- At 00:36, the user tries to use an invalid email address again. The same thing happens as before.
- At 00:42, the user tries to login with an account that doesn't exist. This is rejected by the server and the user receives a notice.
- At 00:50, the user logs in successfully.
- At 00:57, the user creates a conversation for themselves and one more person. This appears in the conversations list.
- At 01:12, the user writes and sends a message in the conversation. The input box clears upon sending to inform the user that it has been sent and the message appears upon refreshing.
- At 01:22, the user receives a response that appears on the other side of the screen. This indicates it wasn't sent by them.
- At 01:47, the user refreshed their conversations and finds that they've been added to a conversation. The conversation appears in the list and the user clicks it.
- At 01:51, the user views the participants in the conversation. Their own email and one other person's is shown.
- At 02:07, the user creates a conversation with three members and it appears in the conversations list.
- At 02:34, the user views the participants in the conversation and confirms that there are, indeed, three people there.

To summarise, this video confirms the following things:

- Account validation works
- Conversations can be created
  - More than two people can be present in a conversation
- Messages can be sent
- Messages can be received
- The participants in a conversation can be viewed

## Other details

The server has been running for around a month with moderately frequent activity and has not been observed to crash or mismanage data in any way.

## Debugging client

Developing a server and a client side-by-side meant that one would often have support for a feature before the other, making it difficult to test things. My solution to this was to make a second, lightweight client that can be run on the command line.

This project is called `echo-cli`, and it was useful for testing server functionality before the main client caught up in features. Being a debugging tool, it is not ideal for day-to-day use but it helped speed development up.

I would use this client to send and retrieve messages as raw requests. This allowed me to not get caught up in the design of the app and directly verify whether a server response looks as expected.
