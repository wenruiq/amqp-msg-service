export const elements = {
    searchInput: document.querySelector('.search__field'),
    searchForm: document.querySelector('.search'),
    searchResList: document.querySelector('.results__list'),
    closeSearch: document.getElementById('close--search'),
    profileBar: document.getElementById('profile--bar'),
    profBar: document.getElementById('prof--bar'),
    msgInput: document.querySelector('.message__field'),
    msgForm: document.querySelector('.message-tray'),
    topBar: document.getElementById('top-bar'),
    msgList: document.querySelector('.message__list'),
    msgBtn: document.getElementById('msg--btn'),
    grpBtn: document.getElementById('grp--btn'),
    createGrp: document.getElementById('create--grp'),
    closeGrp: document.getElementById("close--grp"),
    grpInput: document.querySelector('.grp__field'),
    initLocation: document.getElementById('init--location'),
    searchBox: document.querySelector('.search-box'),
    searchLocationBox: document.querySelector('.location-search-box'),
    closeLocation: document.getElementById("close--location"),
    locationForm: document.querySelector('.search--location'),
    locationInput: document.querySelector('.search__location__field')
};


export const API = {
    login: "https://cors-anywhere.herokuapp.com/http://esdosmessaging.tk:8000/esdos/login/current-user", // Get current-user details {userID, username, fullname, picture}
    getUser: "http://esdosmessaging.tk:8000/api/user", // Get user details {fullname, ipaddress, picture, userID, username} 
    searchUsers: "http://esdosmessaging.tk:8000/api/user/search", // Wildcard search results:[{fullname, ipaddress, picture, userID, username}]
    getAllContacts: "http://esdosmessaging.tk:8000/api/contact", // Get all contacts
    addContact: "https://cors-anywhere.herokuapp.com/http://esdosmessaging.tk:8000/api/contact/create", // POST, {"myID": "hisID"}
    getGroupInfo: "http://esdosmessaging.tk:8000/api/group", // Get group info {grpID, grpname}
    createGroup: "http://esdosmessaging.tk:8000/api/group/create",
    searchLocation: "http://esdosmessaging.tk:8000/api/location/search",
    staticMap: "http://esdosmessaging.tk:8000/api/location/static-map"
};

export const processGoogleName = name => {
    try {
        if (name.endsWith(" _")) {
            return name.slice(0, name.length - 2);
        }
        else {
            return name;
        }
    }catch(err){

    }
}

export const shortenMsg = msg => {
    if (msg.length > 30) {
        const newmsg = msg.slice(0, 30).concat("...")
        return newmsg;
    } else {
        return msg;
    }
}
