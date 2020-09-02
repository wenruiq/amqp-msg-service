#!/usr/bin/env python3

import json
import sys
import os
import datetime
import requests

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')
socketio.connect("http://0.0.0.0:9006")
CORS(app)
'''

from websocket import *

# Communication patterns:
# Use a message-broker with 'topic' exchange to enable interaction
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.

from models import Message

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection\
credentials = pika.PlainCredentials('esdos', 'esdos')
parameters = pika.ConnectionParameters(hostname, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters=parameters)
#connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="order_topic"
channel.exchange_declare(exchange=exchangename, exchange_type='topic')

def consumeMessages():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="messagehost", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='host.send.consume') # bind the queue to the exchange via the key
        # any routing_key with two words and ending with '.message' will be matched

    # set up a consumer and start to wait for coming messages
    #channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    print("AMQP Host Online!")
    print()
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received a message!")
    result = processMessage(json.loads(body))
    # print processing result; not really needed
    #json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator


def processMessage(message):
    print("Processing a message:")
    receiver = message['receiverID']
    sender = message['senderID']

    message = json.dumps(message, default=str) # convert the JSON object to a string
    print(message)

    groupIDarr = getGroups()
    if receiver in groupIDarr:
        print("Receiver is a group!")
        userIDarr = getUsersInGroup(receiver)
        print("Sending to group...")
        for userID in userIDarr:
            if userID != sender:
                routeMessage(userID, message)
    else:
        routeMessage(receiver, message)

    #secondary_transfer(message)

    return message

def routeMessage(receiver, message):
    #routing_key = str(receiver) + '.receive.message'
    hostname = "localhost" # default hostname
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    credentials = pika.PlainCredentials('esdos', 'esdos')
    parameters = pika.ConnectionParameters(hostname, 5672, '/', credentials)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()
    # set up the exchange if the exchange doesn't exist
    exchangename2="order_direct"
    channel.exchange_declare(exchange=exchangename2, exchange_type='direct')
    queuename2= receiver + '.messageclient'
    channel.queue_declare(queue=queuename2, durable=True) # make sure the queue used by the error handler exist and durable
    channel.queue_bind(exchange=exchangename2, queue=queuename2, routing_key=queuename2) # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename2, routing_key=queuename2, body=message,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    )
    print("Message sent to " + queuename2)
    print()

def getGroups():
    url = 'http://localhost:9002/group/get-all-groups'
    response = requests.get(url)
    groupIDarr = []
    for group in response.json()['groups_list']:
        groupIDarr.append(group[0])
    return groupIDarr

def getUsersInGroup(groupID):
    url = 'http://localhost:9002/group/' + str(groupID) + '/members'
    response = requests.get(url)
    userIDarr = []
    for userID in response.json()['members']:
        userIDarr.append(userID)
    return userIDarr





# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is ESDOS : starting message service...")
    
    consumeMessages()
