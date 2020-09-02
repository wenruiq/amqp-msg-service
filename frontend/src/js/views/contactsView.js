import { elements, processGoogleName, shortenMsg } from './base';

// RENDER CONTACT INFO
export const renderContact = contact => {
    // CONDITION IF CONTACT IS A GROUP
    if (contact.grpname) {
        const markup = `
        <div class="group-choco">
            <a class="this-is-grp user-bar-chat user-bar--onhover" href="#${contact.id}" style="text-decoration:none;">
                <img class="profile-image" src="../img/group.png" alt="">
                <div class="text">
                    <h6 class="results__name">${contact.grpname}</h6>
                    <p class="text-muted" id="lastmsg-${contact.id}"></p>
                </div>
                <span class="time text-muted small" id="lastmsg-time-${contact.id}"></span>
            </a>
            <hr>
        </div>
        `;
        elements.searchResList.insertAdjacentHTML('beforeend', markup);
    } else {
        const markup = `
        <div class="private-choco">
            <a class="user-bar-chat user-bar--onhover" href="#${contact.userID}" style="text-decoration:none;">
                <img class="profile-image" src="${contact.picture}" alt="No Picture">
                <div class="text">
                    <h6 class="results__name">${processGoogleName(contact.fullname)}</h6>
                    <p class="text-muted" id="lastmsg-${contact.userID}"></p>
                    <button type="button" class="private-chat btn btn-secondary btn-sm" id="member-selected-${contact.userID}" style="display: none">Select As Group Member</button>
                </div>
                <span class="time text-muted small" id="lastmsg-time-${contact.userID}"></span>              
            </a>
            <hr>
        </div>
        `;
        elements.searchResList.insertAdjacentHTML('beforeend', markup);
    }
};

// RENDER CONTACT LATEST MSG
export const renderContactLatestMsg = () => {
    const allLatestMessages = JSON.parse(localStorage.getItem("allLatestMessages"));
    const contactsWithMessages = JSON.parse(localStorage.getItem("contactsWithMessages"));
    contactsWithMessages.forEach(e => {
        const latestMsg = shortenMsg(allLatestMessages[e].messagetext);
        const msgTimeHr = String(new Date(allLatestMessages[e].datetime).getHours());
        const msgTimeMin = String(new Date(allLatestMessages[e].datetime).getMinutes());
        const msgTime = msgTimeHr.concat(":", msgTimeMin);
        let msgTimeArr = msgTime.split(":");
        if (msgTimeArr[0].length < 2) msgTimeArr[0] = "0".concat(msgTimeArr[0]);
        if (msgTimeArr[1].length < 2) msgTimeArr[1] = "0".concat(msgTimeArr[1]);
        const newMsgTime = msgTimeArr.join(":");
        document.getElementById(`lastmsg-${e}`).innerHTML = latestMsg;
        document.getElementById(`lastmsg-time-${e}`).innerHTML = newMsgTime;
    })
}

// RENDER CONTACT LATEST MSG FROM SOCKET
export const renderContactLatestMsgSocket = json => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const currentUserID = currentUser.userID;
    if (json.senderID == currentUserID || json.receiverID.includes("G")) {
        const id = json.receiverID;
        if (id != '') {
            console.log("Render socket latest!")
            const msg = shortenMsg(json.messagetext);
            let msgTime = json.socketDateTime;
            let msgTimeArr = msgTime.split(":");
            if (msgTimeArr[0].length < 2) msgTimeArr[0] = "0".concat(msgTimeArr[0]);
            if (msgTimeArr[1].length < 2) msgTimeArr[1] = "0".concat(msgTimeArr[1]);
            msgTime = msgTimeArr.join(":");
            document.getElementById(`lastmsg-${id}`).innerHTML = msg;
            document.getElementById(`lastmsg-time-${id}`).innerHTML = msgTime;
        }
    } else {
        const id = json.senderID;
        if (id != '') {
            console.log("Render socket latest!")
            const msg = shortenMsg(json.messagetext);
            let msgTime = json.socketDateTime;
            let msgTimeArr = msgTime.split(":");
            if (msgTimeArr[0].length < 2) msgTimeArr[0] = "0".concat(msgTimeArr[0]);
            if (msgTimeArr[1].length < 2) msgTimeArr[1] = "0".concat(msgTimeArr[1]);
            msgTime = msgTimeArr.join(":");
            document.getElementById(`lastmsg-${id}`).innerHTML = msg;
            document.getElementById(`lastmsg-time-${id}`).innerHTML = msgTime;
        }
    }

}

