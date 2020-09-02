#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
import pika
import requests

# This version of order.py uses a mysql DB via flask-sqlalchemy, instead of JSON files, as the data store.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:EatSomeDick@esdos.cml2qcg6djxv.ap-southeast-1.rds.amazonaws.com:3306/grp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

from models import Group, GroupMembers, User

# Get group for specified grpID
@app.route("/group/<string:grpID>", methods=['GET'])
def get_group(grpID):
    group = db.session.query(Group).filter_by(grpID=grpID).first()
    
    if group:
        return group.json(), 200
        
    else:
        return {'message': 'group not found for id ' + str(grpID)}, 404

# Get list of group members for specified grpID
@app.route("/group/<string:grpID>/members", methods=['GET'])
def get_groupmembers(grpID):
    groupMembers = db.session.query(GroupMembers).filter_by(grpID=grpID)
    if groupMembers:
        return {'members': [member.userID for member in groupMembers]}, 200
    
    else:
        return {'message': 'No members found'}, 404

# Get list of all groups: [ [grpID1, grpname1], [grpID2, grpname2], ... ]
@app.route("/group/get-all-groups", methods=['GET'])
def get_all_groups():
    all_groups = db.session.query(Group).all()
    groups_list = []
    for group in all_groups:
        groups_list.append([group.grpID, group.grpname])
    if len(groups_list) > 0:
        return {'groups_list': groups_list}, 200
    else:
        return {'groups_list': []}, 404

# Get list of groups user is in: [grpID1, grpID2, grpID3, ... ]
@app.route("/group/user-groups/<int:userID>", methods=['GET'])
def get_user_groups(userID):
    groups = db.session.query(GroupMembers).filter_by(userID=userID)
    groupID_list = [group.grpID for group in groups]
    if len(groupID_list) > 0:
        return {'groups:': groupID_list}, 200
    else:
        return {'message': 'User does not exist or user is not in any groups'}, 404

# Update grpname of group
@app.route("/group/change-grpname", methods=['PUT'])
def change_grpname():
    #status in 2xx indicates success
    status = 201
    result = {}

    grpID = request.json.get('grpID', None)
    grpname = request.json.get('grpname', None)

    if grpID != None and grpname != None:      
        group = db.session.query(Group).filter_by(grpID=grpID).first()
        group.grpname = grpname
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid grpID provided"}
    
    if status == 201:
        try:
            db.session.add(group)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occurred when updating the group's groupname in DB.", "error": str(e)}

    if status == 201:
        result = {"status": "success" , "message": "Groupname has been updated successfully"}
    return str(result), status

# Add user to existing group
@app.route("/group/add-user", methods=['POST'])
def add_user():
    status = 201
    result = {}

    userID = request.json.get('userID', None)
    grpID = request.json.get('grpID', None)

    if userID != None and grpID != None:
        GroupMember = GroupMembers(grpID=grpID, userID=userID)
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid grpID or userID"}
    
    if status == 201:
        try:
            db.session.add(GroupMember)
            addContact(userID, grpID)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occured when adding member into group in DB", "error": str(e)}
    
    if status == 201:
        result = {"status": "success" , "message": "Group member added successfully"}
    return str(result), status

# Delete user from existing group
@app.route("/group/delete-user", methods=['DELETE'])
def delete_user():
    status = 201
    result = {}

    userID = request.json.get('userID', None)
    grpID = request.json.get('grpID', None)

    if userID != None and grpID != None:
        GroupMember = db.session.query(GroupMembers).filter_by(userID=userID, grpID=grpID).first()
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid grpID or userID"}
    
    if status == 201:
        try:
            db.session.delete(GroupMember)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occured when deleting member from group in DB", "error": str(e)}
    
    if status == 201:
        result = {"status": "success" , "message": "Group member deleted successfully"}
    return str(result), status

@app.route("/group/create", methods=['POST'])
def create_group():
    #status in 2xx indicates success
    status = 201
    result = {}

    # groupID auto incremented
    grpname = request.json.get('grpname', None)
    user_id_list = request.json.get('user_id_list', None)

    if grpname != None and user_id_list != None:
        grpCount = len(Group.query.all()) + 1
        grpID = "G" + str(grpCount)
        groupObj = Group(grpID=grpID, grpname=grpname)
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid 'groupname' or no users selected"}

    if status == 201:
        try:
            db.session.add(groupObj)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occurred when creating the group in DB.", "error": str(e)}

    # if successfully created group in group db, go on to create groupMembers in groupMembers db
    if status == 201:
        try:
            grpID = groupObj.grpID
            for user in user_id_list:
                GroupMember = GroupMembers(grpID=grpID, userID=user)
                db.session.add(GroupMember)
                addContact(user, grpID)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occured when adding members into the group in DB, but the group was successfully created in DB", "error": str(e)}

    if status == 201:
        result = {"status": "success" , "message": "Group with group members has been created successfully"}
    return str(result), status

def addContact(userID, grpID):
    url = 'http://localhost:9004/contact/create/group/' + str(userID)
    response = requests.post(url, json={'grpID': str(grpID)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9002, debug=True)
    
# @app.route("/order", methods=['GET'])
# def get_all():
#     return {'orders': [order.json() for order in Order.query.all()]}
 
# @app.route("/order/<string:order_id>", methods=['GET'])
# def find_by_order_id(order_id):
#     order = Order.query.filter_by(order_id=order_id).first()
#     if order:
#         return order.json()
#     return {'message': 'Order not found for id ' + str(order_id)}, 404
 
# @app.route("/order/", methods=['POST'])
# def create_order():
#     # status in 2xx indicates success
#     status = 201
#     result = {}

#     # retrieve information about order and order items from the request
#     customer_id = request.json.get('customer_id', None)
#     order = Order(customer_id = customer_id)
#     cart_item = request.json.get('cart_item')
#     for index, ci in enumerate(cart_item):
#         if 'book_id' in cart_item[index] and 'quantity' in cart_item[index]:
#             order.order_item.append(Order_Item(book_id = cart_item[index]['book_id'], quantity = cart_item[index]['quantity']))
#         else:
#             status = 400
#             result = {"status": status, "message": "Invalid 'book_id' or 'quantity'."}
#             break

#     if status==201 and len(order.order_item)<1:
#         status = 404
#         result = {"status": status, "message": "Empty order."}

#     if status==201:
#         try:
#             db.session.add(order)
#             db.session.commit()
#         except Exception as e:
#             status = 500
#             result = {"status": status, "message": "An error occurred when creating the order in DB.", "error": str(e)}
        
#         if status==201:
#             result = order.json()

#     # FIXME: add a call to "send_order" copied from another appropriate file
#     send_order(result)
#     return str(result), status


# def send_order(order):
#     """inform Shipping/Monitoring/Error as needed"""
#     # default username / password to the borker are both 'guest'
#     hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
#     port = 5672 # default messaging port.
#     # connect to the broker and set up a communication channel in the connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
#         # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
#         # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
#     channel = connection.channel()

#     # set up the exchange if the exchange doesn't exist
#     exchangename="order_topic"
#     channel.exchange_declare(exchange=exchangename, exchange_type='topic')

#     # prepare the message body content
#     message = json.dumps(order, default=str) # convert a JSON object to a string

#     # send the message
#     # always inform Monitoring for logging no matter if successful or not
#     # FIXME: is this line of code needed according to the binding key used in Monitoring?
#     # channel.basic_publish(exchange=exchangename, routing_key="shipping.info", body=message)
#         # By default, the message is "transient" within the broker;
#         #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
#         # If need durability of a message, need to declare the queue in the sender (see sample code below).

#     if "status" in order: # if some error happened in order creation
#         # inform Error handler
#         channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
#         channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='*.error') # make sure the queue is bound to the exchange
#         channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=message,
#             properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
#         )
#         print("Order status ({:d}) sent to error handler.".format(order["status"]))
#     else: # inform Shipping and exit
#         # prepare the channel and send a message to Shipping
#         channel.queue_declare(queue='shipping', durable=True) # make sure the queue used by Shipping exist and durable
#         channel.queue_bind(exchange=exchangename, queue='shipping', routing_key='*.order') # make sure the queue is bound to the exchange
#         channel.basic_publish(exchange=exchangename, routing_key="shipping.order", body=message,
#             properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
#             )
#         )
#         print("Order sent to shipping.")
#     # close the connection to the broker
#     connection.close()