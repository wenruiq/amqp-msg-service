from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from os import environ
from sqlalchemy import asc, desc, or_, not_
import eventlet
eventlet.monkey_patch()
import json
import pika
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/message'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')


from models import Message
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


# @app.route("/message", methods=['GET'])
# def get_all():
#     return {'message': [message.json() for message in Message.query.all()]} 

#PROBABLY NOT USING THIS ROUTE RIGHT HERE

@app.route("/message/<string:senderID>", methods=['POST'])  # get ALL messages pertaining to a userID as senderID
def getByID(senderID):
    messages = db.session.query(Message).filter_by(senderID=senderID).order_by(asc(Message.datetime)).all()
    
    if messages:
        return {'message': [message.json() for message in messages]}, 200
        
    else:
        return {'message': 'message not found for id ' + str(senderID)}, 404

@app.route("/message/chats", methods=['POST']) # get all messages sent by the userID, as well as messages sent to the userID
# the array includes groups the user is in
def getByArrayID():
    toReturn = {}
    userIDarr = request.json.get('userIDarr', None)
    for otheruserID in userIDarr:
        if otheruserID[0] == 'G':
            messages = db.session.query(Message).filter(Message.receiverID==otheruserID).order_by(asc(Message.datetime)).all()
            toReturn[otheruserID] = [message.json() for message in messages]
        else:
            messages = db.session.query(Message).filter(or_(Message.senderID==otheruserID, Message.receiverID==otheruserID)).filter(not_(Message.receiverID.contains('G'))).order_by(asc(Message.datetime)).all()
            toReturn[otheruserID] = [message.json() for message in messages]
    return toReturn, 200

@app.route("/message/latest", methods=['POST']) # get latest messages sent by the userID, as well as latest messages sent to the userID
def getByLatestArrayID():
    toReturn = {}
    userIDarr = request.json.get('userIDarr', None)
    for userID in userIDarr:
        if userID[0] == 'G':
            message = db.session.query(Message).filter(Message.receiverID==userID).order_by(desc(Message.datetime)).first()
            toReturn[userID] = message.json()
        else:
            message = db.session.query(Message).filter(or_(Message.senderID==userID, Message.receiverID==userID)).filter(not_(Message.receiverID.contains('G'))).order_by(desc(Message.datetime)).first()
            toReturn[userID] = message.json()
    return toReturn, 200


 
@socketio.on('json')
def send_message(json):
    # status in 2xx indicates success
    status = 201 #created
    result = {}
    print(json)
    messagetext = json['messagetext']
    timestamp = datetime.now()
    senderID = json['senderID']
    receiverID = json['receiverID']
    isLocation = json['isLocation']
    print(messagetext)
    print(senderID)
    print(receiverID)
    print(isLocation)
    #messageID auto incremented
    '''
    messagetext = request.json.get('messagetext', "")
    timestamp = datetime.now()
    senderID = request.json.get('senderID', None)
    receiverID = request.json.get('receiverID', None)
    isLocation = request.json.get('isLocation', False)
    '''
    if senderID != None  and receiverID != None and messagetext.strip() != "":
        # message.messagetext = messagetext
        # message.isLocation = islocation
        # message.receiverID = receiver_ID
        # message.datetime = datetime
        message = Message(senderID = senderID, datetime = timestamp, receiverID = receiverID, isLocation = isLocation, messagetext = messagetext)
        status = 201
        to_be_added = message.json()
    else:
        status = 400
        message = {"status": status, "message": "Invalid 'senderID', 'receiverID' or  empty 'messagetext'."}

    if status==201:
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occurred when creating the order in DB.", "error": str(e)}
        
        if status==201:
            result = to_be_added
            AMQP_send_message(to_be_added)
    print(str(result))
    return str(result), status



def AMQP_send_message(message):
    hostname = "esdosmessaging2.tk"
    #hostname = "18.141.145.79" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.

    credentials = pika.PlainCredentials('esdos', 'esdos')

    parameters = pika.ConnectionParameters(hostname, 5672, '/', credentials)
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    connection = pika.BlockingConnection(parameters)
    # connect to the broker and set up a communication channel in the connection
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="order_topic"
    channel.exchange_declare(exchange=exchangename, exchange_type='topic')
    
    # prepare the message body content
    message = json.dumps(message, default=str) # convert a JSON object to a string


    # prepare the channel and send a message
    channelqueue = channel.queue_declare(queue='messagehost', durable=True) # make sure the queue used by Shipping exist and durable
    #channel.queue_declare(queue='consumemessage', durable=True) # make sure the queue used by Shipping exist and durable
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.send.consume') # make sure the queue is bound to the exchange
    #channel.basic_publish(exchange=exchangename, routing_key="send.message", body=message,
    #channel.queue_declare(queue='consumemessage', durable=True) # make sure the queue used by Shipping exist and durable
    #channel.queue_bind(exchange=exchangename, queue='consumemessage', routing_key='*.send.message') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="host.send.consume", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
        )
    )
    # close the connection to the broker
    connection.close()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
    #app.run(host="0.0.0.0", port=9001, debug=True)
