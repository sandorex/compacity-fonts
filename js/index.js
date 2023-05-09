'use strict';

const CONTENT = document.getElementById('content');
const FONT_SELECT = document.getElementById('font-select');
const TEXT_SELECT = document.getElementById('text-select');

let lastFont = '';

fetch('../data.json')
    .then((response) => response.json())
    .then((json) => {
        json['fonts'].forEach(e => {
            // adds spaces before each capital letter and before and after hyphens
            FONT_SELECT.add(new Option(e.replace('-', ' - ').replace(/([A-Z])/g, ' $1').trim(), e));
        });

        json['texts'].forEach(e => {
            // replace hyphens with spaces and prepend the path and extension
            // so the logic below need not be changed if format changes
            TEXT_SELECT.add(new Option(e.replaceAll('-', ' '), "../texts/" + e + ".html"))
        });

        // TODO: integrate https://meme-api.com/gimme
    });

function getFont() {
    return CONTENT.children[0].style.fontFamily;
}

function setFont(font) {
    lastFont = getFont();
    CONTENT.children[0].style.fontFamily = font;
}

function updateFontSelect() {
    [...FONT_SELECT.options].some((option, index) => {
        if (!option.hidden && option.value == getFont()) {
            FONT_SELECT.selectedIndex = index;
            return true;
        }
    });
}

function btnSwap() {
    setFont(lastFont);
    updateFontSelect();
}

function btnBold(value) {
    if (value === true)
        CONTENT.style.fontWeight = 'bold';
    else
        CONTENT.style.fontWeight = '';
}

function btnItalics(value) {
    if (value === true)
        CONTENT.style.fontStyle = 'italic';
    else
        CONTENT.style.fontStyle = '';
}

function selectFont(selectEl) {
    setFont(selectEl.selectedOptions[0].value)
}

function selectText(value) {
    if (value == "")
        return;

    fetch(value)
        .then(response => response.text())
        .then(data => {
            // clear the children
            CONTENT.textContent = '';

            // insert new content
            CONTENT.innerHTML = data;
        });

    // remove all the memes q.q
    Array.from(document.getElementsByClassName('meme')).forEach(e => e.remove());
}
