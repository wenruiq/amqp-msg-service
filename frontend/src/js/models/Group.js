import axios from 'axios';
import { elements, API } from '../views/base';

export default class Group {
    constructor() {
        this.selectedMembers = [];
        this.grpname = "";
    }

    // Create group
    async createGroup() {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const userID = currentUser.userID;
        this.selectedMembers.push(userID);
        console.log(`Group to be created with name ${this.grpname}`);
        console.log("These are the selected members for the group:");
        console.log(this.selectedMembers);
        const members = this.selectedMembers;
        const name = this.grpname;
        const serviceURL = "https://cors-anywhere.herokuapp.com/http://esdosmessaging.tk:8000/api/group/create";
        try {
            const res = await axios.post(serviceURL, {
                "grpname": name,
                "user_id_list": members
            });
        } catch (err) {
            console.log(`Group.js createGroup Error: ${err}`);
        }
    }
}