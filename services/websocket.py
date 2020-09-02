#!/usr/bin/env python3

# This is the socket file running on AWS to handle message transfer

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import platform
import json
import sys

online_user_socket_pairings = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

@socketio.on('message') # DEFAULT SOCKET RECEIVER
def handle_message(event):
    print("New event: " + event)

@socketio.on('registration') # 2 PARAM
def handle_registration(userID,socketid):
    online_user_socket_pairings[userID] = socketid
    print("This is the pairing")
    print(str(userID) + '=' + str(socketid))
    print(online_user_socket_pairings)

@socketio.on('logout')
def handle_log_out(userID):
    online_user_socket_pairings.pop(userID, None)
    print("Logged out, user removed from online storage")
    print(online_user_socket_pairings)


@socketio.on('checkonline')
def check_if_friend_is_online(contactID):
    if contactID in online_user_socket_pairings:
        emit('verifyonline',online_user_socket_pairings[contactID])
        print("sent back value " + online_user_socket_pairings[contactID])
    else:
        emit('verifyonline',0)
        print("sent back value 0")


@socketio.on('transfermsg', namespace='/private')
def transfer_message_to_both(messagejson, receiver):

    if(receiver in online_user_socket_pairings):
        receiver_room = online_user_socket_pairings[receiver]

        if(receiver_room != None):
            print("message sent to " + receiver + " room at " + receiver_room)
            emit('newmessage', messagejson, room=receiver_room)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=9006, debug = True)