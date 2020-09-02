import axios from 'axios';
import { elements, API } from '../views/base';
import * as messagesView from '../views/messagesView';
import * as contactsView from '../views/contactsView';

export default class Socket {
    constrcutor() {
    }
    socketInit() {

        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const ip = currentUser.ipaddress;
        const currentUserID = currentUser.userID;
        console.log(`The current user's ip is ${ip}`);
        console.log("----------------------------------------------------------------");

        // MY WEB SOCKET
        this.webSocket = io(`http://esdosmessaging2.tk:9006`, { "force new connection": true });
        this.webSocket.on('connect', () => {
        });

        // MY WEB PRIVATE SOCKET
        this.webPrivateSocket = io(`http://esdosmessaging2.tk:9006/private`, { "force new connection": true });
        this.webPrivateSocket.on('connect', () => {
            localStorage.setItem('myWebPrivateSocketID', this.webPrivateSocket.id);
            const myWebPrivateSocketID = localStorage.getItem("myWebPrivateSocketID");
            console.log(`Connected, Web Private Socket ID is: ${myWebPrivateSocketID}`);
            console.log("----------------------------------------------------------------");
            // REGISTER
            this.webSocket.emit('registration', currentUserID, myWebPrivateSocketID);
        });
        // SOCKET TO RECEIVE MESSAGES
        this.webPrivateSocket.on('newmessage', function (json) {
            // RENDER MSG IN MESSAGE BOX 
            messagesView.renderSocketMsg(json);
            // RENDER MSG IN CONTACT BOX
            contactsView.renderContactLatestMsgSocket(json);
        });

        // MY SOCKET
        this.socket = io(`http://${ip}:5001`);
        this.socket.on('connect', () => {
            console.log(`Connected, MY Socket ID is: ${this.socket.id}`);
            console.log("----------------------------------------------------------------");
            localStorage.setItem('mySocketID', this.socket.id);
        });
    }
};