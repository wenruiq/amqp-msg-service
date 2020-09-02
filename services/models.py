from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:EatSomeDick@esdos.cml2qcg6djxv.ap-southeast-1.rds.amazonaws.com:3306/'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# db = SQLAlchemy(app)
from settings import db
# CORS(app)

# user table on RDS needs to be updated
# database.sql needs to be updated

class User(db.Model):
    __tablename__ = 'user'
    # userID = db.Column(mysql.INTEGER(64), primary_key=True) #google id of user
    userID = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    fullname = db.Column(db.String(64), nullable=False)
    picture = db.Column(db.String(300), nullable=False)
    ipaddress = db.Column(db.String(32), nullable=True, default=None)

    def json(self):
        return {'userID' : self.userID, 'username' : self.username, 'fullname' : self.fullname, 'picture' : self.picture, 'ipaddress':self.ipaddress}
            
    def get_userID(self):
        return (self.userID)
    
    def get_username(self):
        return (self.username)
    
    def get_fullname(self):
        return (self.fullname)
    
    def get_picture(self):
        return (self.picture)

    def get_ipaddress(self):
        return (self.ipaddress)


class Message(db.Model):
    __tablename__ = 'message'
    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.String(64), db.ForeignKey('user.userID'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    messagetext = db.Column(db.String(1000), nullable=False)
    isLocation = db.Column(db.Boolean, nullable=False)
    receiverID = db.Column(db.String(64), db.ForeignKey('user.userID'), nullable=False)

    sender = db.relationship('User', foreign_keys=[senderID])
    receiver = db.relationship('User', foreign_keys=[receiverID])

    def json(self):
        return {'messageID': self.messageID, 'senderID': self.senderID, 'datetime': self.datetime,'messagetext': self.messagetext, 'isLocation': self.isLocation, 'receiverID': self.receiverID}
    


class Group(db.Model):
    __tablename__ = 'grp'
 
    grpID = db.Column(db.String(32), primary_key=True)
    grpname = db.Column(db.String(32), nullable=False)

    def json(self):
        return {
            'grpID': self.grpID, 
            'grpname': self.grpname
        }

class GroupMembers(db.Model):
    __tablename__ = 'grpUsers'

    grpID = db.Column(db.String(32),db.ForeignKey('grp.grpID'), primary_key=True, nullable=False)
    userID = db.Column(db.String(64),db.ForeignKey('user.userID'), primary_key=True, nullable=False)

    group = db.relationship('Group', foreign_keys=[grpID])
    user = db.relationship('User', foreign_keys=[userID])

    def json(self):
        return {
                'groupID': self.grpID, 
                'userID': self.userID
        }


class Contact(db.Model):
    __tablename__ = 'contact'
 
    userID = db.Column(db.String(64), primary_key=True, nullable = False)
    contactID = db.Column(db.String(64), primary_key=True, nullable=False)

    def json(self):
        return {
            'userID': self.userID, 
            'contactID': self.contactID
        }