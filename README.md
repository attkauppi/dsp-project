# dsp-project
Distributed Systems project

## How to run the project

Start the project as server:

```
$ python src/main.py
```

Select `s` in the following, the output should look like this:

```
Start as server or client? (s/c): s
Server started on TCP port 3131 and UDP port 5151
```

You're now ready to start a client instance of the project. Run the same command again, but with the following changes:

```
$ python src/main.py
Start as server or client? (s/c):
$ c
$ Enter server IP: 127.0.0.1
```

Now you should get an ouput like this:

```
1. Register
2. Login
3. Send Message
4. Logout
5. Exit
```

To be be able to use the project you first need to register and then login. Then you should be able to send messages. To be able to verify that messages are sent, open two client instances and register two different users.
