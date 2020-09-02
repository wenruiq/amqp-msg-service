import axios from 'axios';
import { elements, API } from '../views/base';

export default class Contacts {
    constructor() {
    }
    // GET ALL CONTACT IDS
    async getAllContacts() {
        const contactList = [];
        try {
            const currentUser = JSON.parse(localStorage.getItem('currentUser'));
            const userID = currentUser.userID;
            const res = await axios(`${API.getAllContacts}/${userID}`);
            res.data.contacts.forEach(e => {
                contactList.push(e);
            })
            this.allContactIDs = res.data.contacts;
            localStorage.setItem('allMyContacts', JSON.stringify(contactList));
        } catch (err) {
            console.log(`Contacts.js getAllContacts Error: ${err}`);
        }
    }

    // GET ALL USER DATA & STORE IN LS
    async getAllUsersData() {
        try {
            const res = await axios(`${API.getUser}/get-all-users`);
            const allUsers = res.data.users;
            allUsers.forEach(e => {
                localStorage.setItem(e.userID, JSON.stringify(e));
            })
        } catch (err) {
            console.log(`Contact.js getAllUsersData Error: ${err}`);
        }
    }

    // GET CONTACT INFO BY ID & STORE IN LS
    async getContactData(id) {
        // If is group ID
        if (id.slice(0, 1) == 'G') {
            const grpObj = { members: [] };
            try {
                const resInfo = await axios(`${API.getGroupInfo}/${id}`);
                grpObj.grpname = resInfo.data["grpname"];
                const resMem = await axios(`${API.getGroupInfo}/${id}/members`);
                resMem.data.members.forEach(e => {
                    grpObj.members.push(e);
                });
                grpObj.id = id;
                this.contactInfo = grpObj;
                localStorage.setItem(id, JSON.stringify(grpObj));
            } catch (err) {
                console.log(`Contact.js getContactData Error: ${err}`)
            }
        } else {
            try {
                const res = await axios(`${API.getUser}/${id}`);
                this.contactInfo = res.data;
                localStorage.setItem(id, JSON.stringify(res.data));

            } catch (err) {
                console.log(`Contact.js getContactData Error: ${err}`);
            }
        }
    }

    // Add contact by ID
    async addContact(hisID) {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const userID = currentUser.userID;
        const serviceURL = `${API.addContact}/${userID}`; //
        try {
            const res = await axios({
                method: "POST",
                url: serviceURL,
                data: { "userID": hisID }
            }
            );
        } catch (err) {
            console.log(`Contact.js addContact Error: ${err}`);
        }
    }
}