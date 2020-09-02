from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import environ

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/message'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Message(db.Model):
    __tablename__ = 'message'
    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.String(64), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    messagetext = db.Column(db.String(1000), nullable=False)
    isLocation = db.Column(db.Boolean, nullable=False)
    receiverID = db.Column(db.String(64), nullable=False)


    def json(self):
        return {'messageID': self.messageID, 'senderID': self.senderID, 'datetime': self.datetime,'messagetext': self.messagetext, 'isLocation': self.isLocation, 'receiverID': self.receiverID}
    
