import { elements } from './base';
import { controlPrepGrp } from '../index';
import * as groupView from './groupView';

export const loadProfileBar = (loginResult) => {
    document.getElementById('pepe-block').style.display = "none";
    const markup = `
    <div class="icons-tray" id="prof--bar" style="display:block">
    <div class="user-bar no-gutters user-bar--grey">
        <img class="profile-image" src="${loginResult.picture}" alt="Profile img">
        <div class="text">
            <h6 class="">${loginResult.fullname}</h6>
            <p class="text-muted">${loginResult.username}</p>
        </div>
        <span class="icons-tray--right">
            <i class="material-icons" id="grp--btn">group_add</i>           
        </span>
        </div>
    </div>
    `;
    elements.profileBar.insertAdjacentHTML('afterbegin', markup);

}

