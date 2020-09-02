import { elements } from './base';


export const getInput = () => elements.locationInput.value;

export const clearInput = () => elements.locationInput.value = '';

export const clearResults = () => {
    const locationResArr = Array.from(document.querySelectorAll('.location-choco'));
    locationResArr.forEach(el => {
        el.style.display = "none";
    })
};


export const renderLocation = location => {
    console.log("rendering location...");
    const markup = `
    <div class="location-choco">
    <div class="user-bar">
        <div class="text" style="width: 90%">
            <h6 class="results__name">${location.description}</h6>
            <p class="text-muted">${location.address}</p>
        </div>
        <i class="material-icons" style="align-self:center; zoom:130%" id="lock-${location.place_id}">my_location</i>
    </div>
    </div>
    `;
    elements.searchResList.insertAdjacentHTML('beforeend', markup);
}

export const renderLocations = locations => {
    locations.forEach(renderLocation);
}

export const initLocation = () => {
    const allPriv = Array.from(document.querySelectorAll('.private-choco'));
    const allGrp = Array.from(document.querySelectorAll('.group-choco'));
    allPriv.forEach(el => {
        el.style.display = "none";
    })
    allGrp.forEach(el => {
        el.style.display = "none";
    })
    elements.searchBox.style.display = "none";
    elements.searchLocationBox.style.display = "block";
    elements.closeLocation.style.visibility = "visible"

}

export const closeLocation = () => {
    const allPriv = Array.from(document.querySelectorAll('.private-choco'));
    const allGrp = Array.from(document.querySelectorAll('.group-choco'));
    allPriv.forEach(el => {
        el.style.display = "block";
    })
    allGrp.forEach(el => {
        el.style.display = "block";
    })
    elements.searchBox.style.display = "block";
    elements.searchLocationBox.style.display = "none";
    elements.closeLocation.style.visibility = "hidden"
    const locationResArr = Array.from(document.querySelectorAll('.location-choco'));
    locationResArr.forEach(el => {
        el.style.display = "none";
    })

}