import axios from 'axios';
import { elements, API } from '../views/base';

export default class Search{
    constructor(query){
        this.query = query;
    }
    async getResults(){
        const res = await axios(`${API.searchUsers}/${this.query}`);
        this.result = res.data.results;
    }catch(err){
        console.log(`Search.js getResults Error: ${err}`);
    }
}