import axios from 'axios';
import { elements, API } from '../views/base';

export default class Location{
    constructor(query){
        this.query = query;
    }
    async getResults(){
        const res = await axios(`${API.searchLocation}/${this.query}`);
        this.result = res.data.predictions;
    }catch(err){
        console.log(`Search.js getResults Error: ${err}`);
    }
    async getStaticMap(placeID){
        const res = await axios(`${API.staticMap}/${placeID}`);
        console.log(res.data);
        return res.data;
    }
    
}