#!/usr/bin/env python3

from datetime import datetime
import json
import pika

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import urllib

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/user'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:EatSomeDick@esdos.cml2qcg6djxv.ap-southeast-1.rds.amazonaws.com:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

from models import User

# Get user by userID
@app.route("/user/<string:userID>", methods=['GET'])
def get_user(userID):
    user = db.session.query(User).filter_by(userID=userID).first()
    if user:
        return user.json(), 200
    else:
        return {'message': 'user not found for id ' + str(userID)}, 404

# Get all users
@app.route("/user/get-all-users", methods=['GET'])
def get_all_users():
    return jsonify({"users": [user.json() for user in db.session.query(User).all()]}), 200

# Get user info given a list of userIDs
@app.route("/user/get-selected-users", methods=['POST'])
def get_selected_users():
    users = request.get_json()["users"]
    user_info_list = []
    for userID in users:
        user = db.session.query(User).filter_by(userID=str(userID)).first()

        if user:
            user_info_list.append(user.json())
        else:
            return {'message': 'user not found for id ' + str(userID)}, 404
    return jsonify({"user_info": user_info_list}), 200

# Search for user by username or fullname
@app.route("/user/search/<string:searchstr>", methods=['GET'])
def search(searchstr):
    searchstr = urllib.parse.unquote(searchstr)
    results = db.session.query(User).filter(User.username.contains(searchstr.lower()) | User.fullname.contains(searchstr.upper())).all()
    return jsonify({"results": [user.json() for user in results]}), 200

# Search for userID by EXACT username or fullname
@app.route("/user/search/exact/<string:searchstr>", methods=['POST'])
def searchExact(searchstr):
    searchstr = urllib.parse.unquote(searchstr)
    results = db.session.query(User).filter_by(username=searchstr).first()
    return results.userID , 200


# Add user
@app.route("/user/<string:userID>", methods=['POST'])
def add_user(userID):
    if (db.session.query(User).filter_by(userID=userID).first()):
        return jsonify({"message": "A user with id '{}' already exists.".format(userID)}), 400
    data = request.get_json()
    user = User(userID=userID, username=data["username"], fullname=data["fullname"], picture=data["picture"])
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "An error occurred creating the user.", "error": str(e)}), 500
    return jsonify(user.json()), 201

# Change profile pic URL
@app.route("/user/picture/<string:userID>", methods=['POST'])
def change_picture(userID):
    user = db.session.query(User).filter_by(userID=userID).first()
    if not user:
        return jsonify({"message": "User with id '{}' does not exist.".format(userID)}), 400
    data = request.get_json()
    user.picture = data["picture"]
    db.session.commit()
    return jsonify(user.json()), 201

@app.route("/user/ip", methods=['POST'])
def setIP():
    data = request.get_json()
    userID = data['userID']
    user = db.session.query(User).filter_by(userID=userID).first()

    user.ipaddress = data['ipAddress']
    db.session.commit()
    return jsonify(user.json()), 200

@app.route("/user/ip", methods=['GET'])
def getIP():
    data = request.get_json()
    userID = data['userID']
    user = db.session.query(User).filter_by(userID=userID).first()

    return jsonify({"ipAddress":user.ipaddress}) , 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9005, debug=True)