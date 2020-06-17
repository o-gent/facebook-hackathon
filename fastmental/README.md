# FASTMENTAL docs

# stage 1: Handle message from FB server

All incoming communication is handled through the fastapi sever which is created in __init__.py

Messenger webhooks are in routers/messenger.py

When a message is sent to the server:
- The messages are parsed 
- people_handler.handle_message() is called with the message parameters

# stage 2: Fetch the information for the person sending the message

This is all managed in people_handler which is effectively an interface to the correct person class

The persons handle_message() method is called

# stage 3: Process the persons text and respond correctly

This is handled by the person class when handle_message() method is called. Returns text and quick response options

# stage 4: send a response message to the FB server

people_handler calls response/fb_message()

