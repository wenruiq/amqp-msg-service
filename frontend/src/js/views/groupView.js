import { elements } from './base';
import * as loginView from './loginView';


export const renderGrpBar = () => {
    document.getElementById('prof--bar').style.display = "none";
    document.getElementById("grp-tray").style.display = "block";
    const grpChats = Array.from(document.querySelectorAll('.group-choco'));
    grpChats.forEach(el => {
        el.style.display = "none";
    })

};

export const displayMemSelect = () => {
    const memArr = Array.from(document.querySelectorAll('.private-chat'));
    memArr.forEach(el => {
        el.style.display = "block";
    })
}


export const hideMemSelect = () => {
    const memArr = Array.from(document.querySelectorAll('.private-chat'));
    memArr.forEach(el => {
        el.style.display = "none";
    })
}

export const showGrps = () => {
    const grpChats = Array.from(document.querySelectorAll('.group-choco'));
    grpChats.forEach(el => {
        el.style.display = "block";
    })
};

export const getInput = () =>{
    if (elements.grpInput.value == ''){
        return   "Group ".concat(Math.floor(Math.random() * 1000));
    }
    return elements.grpInput.value;
}

export const clearInput = () =>{
    elements.grpInput.value = '';
}

export const grpComplete = () => {
    document.getElementById('prof--bar').style.display = "block";
    document.getElementById("grp-tray").style.display = "none";
    hideMemSelect();
    const grpChats = Array.from(document.querySelectorAll('.group-choco'));
    grpChats.forEach(el => {
        el.style.display = "block";
    })
}