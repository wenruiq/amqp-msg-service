from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import environ
import json
import pika
#import doqu
import requests

# This version of order.py uses a mysql DB via flask-sqlalchemy, instead of JSON files, as the data store.

from models import Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secret!'

db = SQLAlchemy(app)
CORS(app)

'''
class Message:
    def __init__(self, senderID, datetime, receiverID, isLocation, messagetext):
        #self.messageID = messageID
        self.senderID = senderID
        self.datetime = datetime
        self.receiverID = receiverID
        self.isLocation = isLocation
        self.messagetext = messagetext
'''

def processMessage(message):
    #app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/message'
    #app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #app.config['SECRET_KEY'] = 'secret!'

    #db = SQLAlchemy(app)
    #CORS(app)

    messagetext = message['messagetext']
    timestamp = message['datetime']
    senderID = message['senderID']
    receiverID = message['receiverID']
    isLocation = message['isLocation']
    message = Message(senderID = senderID, datetime = timestamp, receiverID = receiverID, isLocation = isLocation, messagetext = messagetext)
    status = 201
    print()
    try:
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        status = 500
        result = {"status": status, "message": "An error occurred when creating the order in DB.", "error": str(e)}

    if status==201:
            result = message.json()

    print(str(result))

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Incoming message!")
    processMessage(json.loads(body))
    print("Message added.")
    print()
    print()

def main(userID):
    hostname = "esdosmessaging2.tk" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.

    credentials = pika.PlainCredentials('esdos2', 'esdos2')

    #parameters = pika.ConnectionParameters(host=hostname, port = port, virtual_host= "/", credentials=credentials)
    parameters = pika.ConnectionParameters(hostname, 5672, '/', credentials)

    #connection = pika.BlockingConnection(parameters=parameters)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    routing_key = str(userID) + '.receive.message'

    # set up the exchange if the exchange doesn't exist
    exchangename="order_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare a queue for receiving messages
    queuename = userID + '.messageclient'
    channel.queue_declare(queue=queuename, durable=True) # 'durable' makes the queue survive broker  restarts
    channel.queue_bind(exchange=exchangename, queue=queuename, routing_key=queuename) # bind the queue to the exchange via the key
        # any routing_key ending with '.message' will be matched

    # set up a consumer and start to wait for coming messages
    print()
    channel.basic_consume(queue=queuename, on_message_callback=callback, auto_ack=True)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

        
'''
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
'''

if __name__ == '__main__':
    print("Connecting to ESDOS server...")
    username = environ.get('username')
    
    url = 'http://esdosmessaging.tk:8000/api/user/search/exact/' + str(username)
    response = requests.post(url)
    userID = response.text
    if not response.ok:
        print("Username error!")
    else:
        ipAddress = environ.get('ipAddress')
        url = 'http://esdosmessaging.tk:8000/api/user/ip'
        requests.post(url, json={'userID':userID, 'ipAddress':str(ipAddress)})
        if not response.ok:
            print("Ip Error!")
        else:
            main(userID)
    #socketio.run(app, host="127.0.0.1", port=5001, debug=True)