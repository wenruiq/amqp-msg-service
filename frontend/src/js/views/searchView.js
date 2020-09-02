import { elements, processGoogleName } from './base';

export const getInput = () => elements.searchInput.value;

export const clearInput = () => elements.searchInput.value = '';

export const clearResults = () => {
    elements.searchResList.innerHTML = '';
};

const renderUser = user => {
    const markup = `
    <div class="user-bar">
        <img class="profile-image" src="${user.picture}" alt="../img/pepefriend.jpg">
        <div class="text">
            <h6 class="results__name">${processGoogleName(user.fullname)}</h6>
            <p class="text-muted">Username: ${user.username}</p>
        </div>
        <i class="material-icons" id="add${user.userID}">person_add</i>
    </div>
    <hr>
    `;
    elements.searchResList.insertAdjacentHTML('beforeend', markup);
}

export const renderSearch = users => {
    users.forEach(renderUser);
}

export const showCloseSearch = () => {
    elements.closeSearch.style.display = '';
    elements.closeSearch.style.visibility = "visible"
}

export const hideCloseSearch = () => {
    elements.closeSearch.style.display = 'none';
}