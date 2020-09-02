import axios from 'axios';
import { elements, API } from '../views/base';

export default class Login {
    constructor(id) {
        this.id = id
    }
    async getCurrentUserInfo() {
        try {
            console.log(`Getting Current User Info (${this.id})`);
            console.log("----------------------------------------------------------------");
            const res = await axios(`${API.getUser}/${this.id}`);
            this.result = res.data;
        } catch (err) {
            console.log(`Login.js getCurrentUserInfo Error: ${err}`);
        }
    }
}