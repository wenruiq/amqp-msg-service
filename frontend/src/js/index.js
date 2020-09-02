import { elements, API } from './views/base';
import Login from './models/Login';
import Socket from './models/Socket';
import Search from './models/Search';
import Contacts from './models/Contacts';
import Messages from './models/Messages';
import Group from './models/Group';
import Location from './models/Location';
import * as loginView from './views/loginView';
import * as searchView from './views/searchView';
import * as contactsView from './views/contactsView';
import * as messagesView from './views/messagesView';
import * as groupView from './views/groupView';
import * as locationView from './views/locationView';

const state = {};

// TEST INIT (HARDCODED DATA)
const initTest = () => {
    // ADD CURR USER DATA TO LS & LOAD PROFILE
    state.login = new Login();
    state.login.result = {
        // "fullname": "SAMUEL JAMES CHIA _",
        // "ipaddress": "192.168.1.117",
        // "picture": "https://lh4.googleusercontent.com/-bZENX4akeUo/AAAAAAAAAAI/AAAAAAAAAAA/AAKWJJPdAoH7u7lZ_Px63oQeTBM-a4WMKA/photo.jpg",
        // "userID": "100398562385810757969",
        // "username": "samuelchia.2018"
        "fullname": "QU WENRUI _",
        "ipaddress": "192.168.1.118",
        "picture": "https://lh3.googleusercontent.com/a-/AOh14Gjg4ho2EO2vK6brojv4-tl4vU5UeFTxwYu8TBx2BQ",
        "userID": "106407095310475127292",
        "username": "wenrui.qu.2018"
        // "fullname": "PANG QI XUAN _",
        // "ipaddress": "192.168.50.15",
        // "picture": "https://lh6.googleusercontent.com/-hg18P6Snscg/AAAAAAAAAAI/AAAAAAAAAAA/AAKWJJOTy01VVPa5i3GXhBFupdahn7Lyng/photo.jpg",
        // "userID": "116684078650657828897",
        // "username": "qxpang.2018"
    };
    const currentUserInfo = state.login.result;
    localStorage.setItem('currentUser', JSON.stringify(currentUserInfo));
    loginView.loadProfileBar(currentUserInfo);


    // TEST SET UP SOCKETS
    controlSocket();

    // TEST GET ALL CONTACTS & MESSAGES
    controlContacts();

    // TEST SET UP GROUP EVENT LISTENERS
    controlGroupMajor();

    // CONSOLELOG STATE
    console.log("The state is:")
    console.log(state);
    console.log("----------------------------------------------------------------")
};

// ACTUAL INIT
const init = () => {
    // GET USERID FROM QUERY STRING & RETRIEVE CURR USER DATA
    const loggedInID = localStorage.getItem("loggedIn");
    console.log(`User |${loggedInID}| has logged in`)
    console.log("----------------------------------------------------------------");

    // GET CURR USER INFO, SET UP SOCKETS -> CONTACTS -> MESSAGES
    controlLogin(loggedInID);

    // CONSOLELOG STATE
    console.log("The state is:")
    console.log(state);
    console.log("----------------------------------------------------------------");

};

/**
 * LOGIN TO GET CURRENT USER INFO
 */
const controlLogin = async (id) => {
    state.login = new Login(id);
    try {
        // GET CURR USER INFO & STORE IN LS & LOAD PROFILE BAR
        await state.login.getCurrentUserInfo();
        const currentUserInfo = state.login.result;
        loginView.loadProfileBar(currentUserInfo);
        localStorage.setItem('currentUser', JSON.stringify(currentUserInfo));

        // SET UP SOCKETS
        controlSocket();
        // GET CONTACTS & MESSAGES
        controlContacts();
        // SET UP EL FOR GROUP CREATION
        controlGroupMajor();
    } catch (err) {
        console.log(`controlLogin Error: ${err}`);
    }
};

/**
 * SOCKET INIT
 */
const controlSocket = () => {
    state.socket = new Socket();
    state.socket.socketInit();
};

/**
 * GET ALL CONTACTS & MESSAGES
 */
const controlContacts = async () => {
    state.contacts = new Contacts();
    try {
        // Clear chat rooms
        searchView.clearResults();
        // Get all contact IDs
        await state.contacts.getAllContacts();
        state.contacts.allContactIDs.forEach(async (el) => {
            // Get contact info by ID
            await state.contacts.getContactData(el);
            // Render chat room
            contactsView.renderContact(state.contacts.contactInfo);
        });
        // Get all user data (just in case)
        await state.contacts.getAllUsersData();
        // Get all messages after getting contacts
        controlMessages();

    } catch (err) {
        console.log(`controlContacts Error: ${err}`);
    }
};


/**
 *  ADD CONTACT
 */
const addContact = async (hisID) => {
    try {
        await state.contacts.addContact(hisID);
        // Hide close search button
        searchView.hideCloseSearch();
        // Clear search input
        searchView.clearInput();
        controlContacts();
    } catch (err) {
        console.log(`addContact Error: ${err}`);
    }

}
// GLOBAL EL FOR ADD CONTACT BUTTON
window.addEventListener('click', e => {
    if (e.target.matches('.material-icons') && e.target.id.includes("add")) {
        const addID = e.target.id.slice(3);
        addContact(addID);
    }
})



/**
 * SEARCH TO ADD FRIEND
 */
const controlSearch = async () => {
    // Get search query from view
    const query = searchView.getInput();
    if (query) {
        // Add new search obj to state
        state.search = new Search(query);
        // Prep UI
        searchView.clearResults();
        // Search
        try {
            await state.search.getResults();
            // Render results
            searchView.renderSearch(state.search.result);
            // Show cancel search button
            searchView.showCloseSearch();
        } catch (err) {
            console.log(`controlSearch Error: ${err}`);
        }
    }
};
// EL FOR SEARCH FORM
elements.searchForm.addEventListener('submit', e => {
    e.preventDefault();
    controlSearch();
});
// EL TO CLOSE SEARCH & RENDER CHAT ROOMS
elements.closeSearch.addEventListener('click', e => {
    if (e.target.matches(".material-icons") && e.target.id == "close--search") {
        // Reload contact list
        controlContacts();
        // Hide close search button
        searchView.hideCloseSearch();
        // Clear search input
        searchView.clearInput();
    }
});



/**
 * GET ALL MESSAGES
 */
const controlMessages = async (friend) => {
    state.messages = new Messages();
    try {
        await state.messages.getAllMessages();
        await state.messages.getAllLatestMessages();
        // Render window based on id    
        messagesView.renderMessageWindow(friend);
        // RENDER LATEST MSG IN CONTACT LIST
        contactsView.renderContactLatestMsg();
    } catch (err) {
        console.log(`controlMessages Error: ${err}`);
    }
};
// RENDER MSG IN MSG WINDOW ONLY WHEN HASH IS PRESENT/CHANGE
['hashchange', 'load'].forEach(event => window.addEventListener(event, function () {
    const id = window.location.hash.replace('#', '');
    if (id != '') {
        // Get info based on id
        const friend = JSON.parse(localStorage.getItem(id));
        // Get all messages again
        controlMessages(friend);
        // Auto selects msg input field
        elements.msgInput.select();
        // Socket online verifications
        if (state.socket) {
            state.socket.webSocket.emit('checkonline', id);
            state.socket.webSocket.on('verifyonline', function (hisSocketID) {
                console.log(`| Verified that user ${id} | Has a socketID of: ${hisSocketID}|`);
                localStorage.setItem('currChatSocketID', hisSocketID);
                if (hisSocketID != 0) {
                    localStorage.setItem('currChatIsOnline', 'yes');
                } else {
                    localStorage.setItem('currChatIsOnline', 'no');
                }
            })
        }
    }
}));



/*
* SOCKET SEND MESSAGE
*/
const socketSendMsg = (message, isLocation = false) => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const ip = currentUser.ipaddress;
    const currentUserID = currentUser.userID;
    const id = window.location.hash.replace('#', '');
    const mySocketID = localStorage.getItem('mySocketID');
    const receiverSocketID = localStorage.getItem('currChatSocketID');
    const myWebPrivateSocketID = localStorage.getItem('myWebPrivateSocketID');
    console.log(`ReceiverSocket ID: ${receiverSocketID}`)
    console.log(`MyWebPrivateSocket ID: ${myWebPrivateSocketID}`)
    const isOnline = localStorage.getItem('currChatIsOnline');
    if (id.substring(0, 1) == "G") {
        const grpInfo = JSON.parse(localStorage.getItem(id));
        const memArr = grpInfo.members;
        memArr.forEach(e => {

            if (e != currentUserID) {
                console.log(`message sent to ${e}`)
                state.socket.webPrivateSocket.emit('transfermsg', {
                    "messagetext": message,
                    "senderID": currentUserID,
                    "receiverID": id,
                    "isLocation": isLocation,
                    "mySocketID": mySocketID,
                    "receiverSocketID": receiverSocketID,
                    "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))

                }, e);
            }

        })
        state.socket.webPrivateSocket.emit('transfermsg', {
            "messagetext": message,
            "senderID": currentUserID,
            "receiverID": id,
            "isLocation": isLocation,
            "mySocketID": mySocketID,
            "receiverSocketID": receiverSocketID,
            "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
        }, currentUserID);
        state.socket.socket.emit('json', {
            "messagetext": message,
            "senderID": currentUserID,
            "receiverID": id,
            "isLocation": isLocation,
            "mySocketID": mySocketID,
            "receiverSocketID": receiverSocketID,
            "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
        });
        console.log(grpInfo);
    } else {
        if (isOnline == 'yes') {
            state.socket.socket.emit('json', {
                "messagetext": message,
                "senderID": currentUserID,
                "receiverID": id,
                "isLocation": isLocation,
                "mySocketID": mySocketID,
                "receiverSocketID": receiverSocketID,
                "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
            });
            state.socket.webPrivateSocket.emit('transfermsg', {
                "messagetext": message,
                "senderID": currentUserID,
                "receiverID": id,
                "isLocation": isLocation,
                "mySocketID": mySocketID,
                "receiverSocketID": receiverSocketID,
                "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
            }, currentUserID);
            state.socket.webPrivateSocket.emit('transfermsg', {
                "messagetext": message,
                "senderID": currentUserID,
                "receiverID": id,
                "isLocation": isLocation,
                "mySocketID": mySocketID,
                "receiverSocketID": receiverSocketID,
                "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))

            }, id);
        } else {
            state.socket.socket.emit('json', {
                "messagetext": message,
                "senderID": currentUserID,
                "receiverID": id,
                "isLocation": isLocation,
                "mySocketID": mySocketID,
                "receiverSocketID": "offline",
                "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
            });
            state.socket.webPrivateSocket.emit('transfermsg', {
                "messagetext": message,
                "senderID": currentUserID,
                "receiverID": id,
                "isLocation": isLocation,
                "mySocketID": mySocketID,
                "receiverSocketID": receiverSocketID,
                "socketDateTime": String(new Date().getHours()).concat(":", String(new Date().getMinutes()))
            }, currentUserID);
        }
    }

}

/**
 * CONTROL SEND MSG
 */
const controlSendMsg = () => {
    // Get message from input
    const msg = messagesView.getInput();
    // Send message
    socketSendMsg(msg);
    // Clear input from bar
    messagesView.clearInput();
};
// EL for message input
elements.msgForm.addEventListener('submit', e => {
    e.preventDefault();
    if (state.socket) {
        controlSendMsg();
    }
});
// EL for message input btn
elements.msgBtn.addEventListener('click', e => {
    e.preventDefault();
    if (state.socket) {
        controlSendMsg();
    }
});


/**
 * GROUP CONTROLLER (AFTER CURR USER PROF BAR LOADS)
 */
const controlGroupMajor = () => {
    // EL Prepare for group adding
    document.getElementById('grp--btn').addEventListener('click', e => {
        e.preventDefault();
        groupView.renderGrpBar();
        // Create group in state
        state.group = new Group();
        // Display select as friends
        groupView.displayMemSelect();
    });
    document.getElementById('close--grp').addEventListener('click', e => {
        document.getElementById('prof--bar').style.display = "block";
        document.getElementById('grp-tray').style.display = "none";
        state.group.selectedMembers = [];
        state.group.grpname = '';
        groupView.hideMemSelect();
        groupView.showGrps();
        e.preventDefault();
    });
    window.addEventListener('click', e => {
        if (e.target.matches('.private-chat') && e.target.id.includes("member-selected")) {
            const id = e.target.id.slice(16)
            state.group.selectedMembers.push(id);
            console.log(state.group.selectedMembers);
            document.getElementById(e.target.id).style.display = "none";
        }
    })
    elements.createGrp.addEventListener('click', e => {
        e.preventDefault();
        console.log(state.group.selectedMembers);
        addGroup();
    });
}
// ADD GROUP
const addGroup = async () => {
    state.group.grpname = groupView.getInput();
    try {
        await state.group.createGroup();
        groupView.clearInput();
        groupView.grpComplete();
        controlContacts();
    } catch (err) {
        console.log(err);
    }
}

/**
 * CONTROL LOCATION
 */
const controlLocation = async () => {
    // Get search
    const query = locationView.getInput();
    if (query) {
        state.location = new Location(query);
        locationView.clearResults();
        try {
            await state.location.getResults();
            locationView.renderLocations(state.location.result);

        } catch (err) {
            console.log(`controlLocation Error: ${err}`);
        }
    }

};
const controlStatic = async (placeID) => {
    try {
        const staticMsg = await state.location.getStaticMap(placeID);
        socketSendMsg(staticMsg, true);
        locationView.closeLocation();
    } catch (err) {
        console.log(`controlStatic Error: ${err}`);
    }
}
// EL to init location
elements.initLocation.addEventListener('click', e => {
    locationView.initLocation();
    elements.closeLocation.addEventListener('click', e => {
        locationView.closeLocation();
    })
})
// EL search location submitted
elements.locationForm.addEventListener('submit', e => {
    e.preventDefault();
    // control location
    controlLocation();
    locationView.clearInput();
});
// EL Send Location
window.addEventListener('click', e => {
    if (e.target.matches('.material-icons') && e.target.id.includes("lock-")) {
        const placeID = e.target.id.slice(5);
        controlStatic(placeID);
    }
})

// TEST INIT
// initTest();

// ACTUAL APP INIT
init();


