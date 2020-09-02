import axios from 'axios';
import { elements, API } from '../views/base';

export default class Messages {
    constructor() {

    }
    async getAllMessages() {
        const userIDs = [];
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const ip = currentUser.ipaddress;
        const serviceURL = `http://${ip}:5001/message/chats`;
        userIDs.push(currentUser.userID);
        const allMyContacts = JSON.parse(localStorage.getItem("allMyContacts"));
        allMyContacts.forEach(e => {
                userIDs.push(e);
        });
        // console.log(`Getting messages for the following contact IDs:`);
        // console.log(userIDs);
        // console.log("----------------------------------------------------------------");
        try {
            const res = await axios({
                method: "POST",
                url: serviceURL,
                data: { "userIDarr": userIDs }
            }
            );
            localStorage.setItem("allMyMessages", JSON.stringify(res.data));
        } catch (err) {
            console.log(`Message.js getAllMessages Error: ${err}`);
        }
    }

    async getAllLatestMessages() {
        const userIDs = [];
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const ip = currentUser.ipaddress;
        const currentUserID = currentUser.userID;
        const serviceURL = `http://${ip}:5001/message/latest`;
        const allMyContacts = JSON.parse(localStorage.getItem("allMyContacts"));
        const allMessages = JSON.parse(localStorage.getItem("allMyMessages"));
        const contactsWithMessages = [];
        allMyContacts.forEach(e => {
            // Error handling to prevent CORS for now, only check latest message for contacts with messages
            if (allMessages[e].length != 0) {
                userIDs.push(String(e));
                contactsWithMessages.push(e);
            }
        });
        localStorage.setItem("contactsWithMessages", JSON.stringify(contactsWithMessages));
        try {
            const res = await axios({
                method: "POST",
                url: serviceURL,
                data: { "userIDarr": userIDs }
            }
            );
            localStorage.setItem("allLatestMessages", JSON.stringify(res.data));
        } catch (err) {
            console.log(`Messages.js getAllLatestMessages Error: ${err}`);
        }

    }
}