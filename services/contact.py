#!/usr/bin/env python3

from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
from os import environ
from sqlalchemy import desc, or_

from models import Contact

import json
import pika

# This version of order.py uses a mysql DB via flask-sqlalchemy, instead of JSON files, as the data store.

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/contact'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:EatSomeDick@esdos.cml2qcg6djxv.ap-southeast-1.rds.amazonaws.com:3306/contact'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
#from flask_socketio import SocketIO, send, emit

app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/contact/<string:userID>", methods=['GET'])
def getContactsByID(userID):
    contacts = db.session.query(Contact).filter_by(userID=userID).all()
    if contacts:
        return {'contacts': [contact.contactID for contact in contacts]}, 200
    else:
        return {'message': 'contacts not found for id ' + str(userID)}, 404


@app.route("/contact/create/<string:userID>", methods=['POST'])
def createContact(userID):
    status = 201
    result = {}

    contactID = request.json.get('userID', None)

    if contactID != None:
        contact = Contact(userID=userID, contactID=contactID)
        reverseContact = Contact(userID=contactID, contactID=userID)
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid userID"}
    
    if status == 201:
        try:
            db.session.add(contact)
            db.session.add(reverseContact)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occured when adding contact into DB", "error": str(e)}
    
    if status == 201:
        result = {"status": "success" , "message": "Contact added successfully"}
    return str(result), status


@app.route("/contact/create/group/<string:userID>", methods=['POST'])
def createGroupContact(userID):
    status = 201
    result = {}

    contactID = request.json.get('grpID', None)

    if contactID != None:
        contact = Contact(userID=userID, contactID=contactID)
        status = 201
    else:
        status = 400
        result = {"status": status, "message": "Invalid grpID"}
    
    if status == 201:
        try:
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            status = 500
            result = {"status": status, "message": "An error occured when adding contact into DB", "error": str(e)}
    
    if status == 201:
        result = {"status": "success" , "message": "Contact added successfully"}
    return str(result), status

if __name__ == '__main__':
    #socketio.run(app, host="127.0.0.1", port=5001, debug=True)
    app.run(host="0.0.0.0", port=9004, debug=True)
