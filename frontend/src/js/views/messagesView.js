import { elements, processGoogleName } from './base';


export const getInput = () => elements.msgInput.value;

export const clearInput = () => elements.msgInput.value = '';

// Render messages chat window
export const renderMessageWindow = friend => {
    if(friend){
    renderTopBar(friend);
    renderMessagesBox(friend);
    };
};

export const renderTopBar = friend => {
    elements.topBar.innerHTML = '';
    // If group
    if (friend.grpname) {
        const markup = `
        <div class="icons-tray">
            <div class="user-bar no-gutters user-bar--grey">
                <img class="profile-image" src="../img/group.png" alt="">
                <div class="text">
                    <h6 class="">${friend.grpname}</h6>
                    <p class="text-muted">${friend.id}</p>
                </div>
                <!-- <span class="icons-tray--right">
                    <i class="material-icons">icon placeholder</i>
                </span> -->
            </div>
        </div>
        `;
        elements.topBar.insertAdjacentHTML('afterbegin', markup);
    } else {
        const markup = `
        <div class="icons-tray">
            <div class="user-bar no-gutters user-bar--grey">
                <img class="profile-image" src="${friend.picture}" alt="">
                <div class="text">
                    <h6 class="">${processGoogleName(friend.fullname)}</h6>
                    <p class="text-muted">${friend.username}</p>
                </div>
                <!-- <span class="icons-tray--right">
                    <i class="material-icons">icon placeholder</i>
                </span> -->
            </div>
        </div>
        `;
        elements.topBar.insertAdjacentHTML('afterbegin', markup);
    }
};

const msgBoxCalc = (msg) => {
    const length = msg.length;
    if (length < 17) {
        return 4
    } else {
        return 5
    }
}

// RENDER MSG IN MSG BOX
export const renderMessagesBox = friend => {
    elements.msgList.innerHTML = '';
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const currentUserID = currentUser.userID;
    const chatSelectedID = window.location.hash.replace('#', '');
    if (chatSelectedID != '' && JSON.parse(localStorage.getItem("allMyMessages"))) {
        const messages = JSON.parse(localStorage.getItem("allMyMessages"))[chatSelectedID];
        messages.forEach(e => {
            // Messages sent from me to this window (Privat/Group)
            if (e.receiverID == chatSelectedID && e.senderID == currentUserID) {
                const markup = `
            <div class="row no-gutters">
                <div class="col-${msgBoxCalc(e.messagetext)} offset-${12 - msgBoxCalc(e.messagetext)}">
                    <div class="chat-bubble chat-bubble--right">
                        ${e.messagetext}
                    </div>
                </div>
            </div>
            `;
                elements.msgList.insertAdjacentHTML('beforeend', markup);
                elements.msgList.scrollTop = elements.msgList.scrollHeight;
                // Private chat to me
            } else if (e.receiverID == currentUserID && e.senderID == chatSelectedID) {
                const markup = `
                <div class="row no-gutters">
                    <div class="col-${msgBoxCalc(e.messagetext)}">
                        <div class="chat-bubble">
                            ${e.messagetext}
                        </div>
                    </div>
                </div>
                `;
                elements.msgList.insertAdjacentHTML('beforeend', markup);
                elements.msgList.scrollTop = elements.msgList.scrollHeight;
                // Group message by someone else to this channel
            } else if (e.receiverID == chatSelectedID) {
                const msgSenderInfo = JSON.parse(localStorage.getItem(e.senderID));
                const markup = `
                <div class="row no-gutters">
                    <div class="col-${msgBoxCalc(e.messagetext.concat(processGoogleName(msgSenderInfo.fullname)))}">
                        <div class="chat-bubble">
                            <b>${processGoogleName(msgSenderInfo.fullname)}</b>: ${e.messagetext}
                        </div>
                    </div>
                </div>
                `;
                elements.msgList.insertAdjacentHTML('beforeend', markup);
                elements.msgList.scrollTop = elements.msgList.scrollHeight;

            }
            ;
        });
    } else {
        console.log("@ ERROR GETTING MESSAGES@ ");
        console.log("----------------------------------------------------------------");
    }
};

// RENDER SOCKET MSG IN MSG BOX
export const renderSocketMsg = json => {
    console.log("----------------------------------------------------------------");
    console.log("Message received at socket:");
    console.log(json);
    console.log("----------------------------------------------------------------");
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const currentUserID = currentUser.userID;
    const currWindowID = window.location.hash.replace('#', '');
    if (currWindowID != '') {
        // Messages sent from me to this window (Private/Group)
        if (currWindowID == json.receiverID && currentUserID == json.senderID) {
            const markup = `
            <div class="row no-gutters">
                <div class="col-${msgBoxCalc(json.messagetext)} offset-${12 - msgBoxCalc(json.messagetext)}">
                    <div class="chat-bubble chat-bubble--right">
                        ${json.messagetext}
                    </div>
                </div>
            </div>
            `;
            elements.msgList.insertAdjacentHTML('beforeend', markup);
            elements.msgList.scrollTop = elements.msgList.scrollHeight;

            // Private chat sent to me
        } else if (currWindowID == json.senderID && currentUserID == json.receiverID) {
            const markup = `
                <div class="row no-gutters">
                    <div class="col-${msgBoxCalc(json.messagetext)}">
                        <div class="chat-bubble">
                            ${json.messagetext}
                        </div>
                    </div>
                </div>
                `;
            elements.msgList.insertAdjacentHTML('beforeend', markup);
            elements.msgList.scrollTop = elements.msgList.scrollHeight;

            // Group message sent by someone else to this window
        } else if (currWindowID == json.receiverID) {
            console.log("wait what???")
            const msgSenderInfo = JSON.parse(localStorage.getItem(json.senderID));
            console.log(msgSenderInfo);
            const markup = `
            <div class="row no-gutters">
                <div class="col-${msgBoxCalc(json.messagetext.concat(processGoogleName(msgSenderInfo.fullname)))}">
                    <div class="chat-bubble">
                    <b>${processGoogleName(msgSenderInfo.fullname)}</b>: ${json.messagetext}
                    </div>
                </div>
            </div>
            `;
            elements.msgList.insertAdjacentHTML('beforeend', markup);
            elements.msgList.scrollTop = elements.msgList.scrollHeight;

        }
    }
}


