'use strict';

const CONTENT = document.getElementById('content');
const FONT_FAMILY_SELECT = document.getElementById('font-family-select');
const FONT_STYLE_SELECT = document.getElementById('font-style-select');
const TEXT_SELECT = document.getElementById('text-select');

let fontFamilies = [];
let fonts = [];
let texts = [];
let fontTexts = {};

function clearTexts() {
    // remove all options
    while (TEXT_SELECT.options.length)
        TEXT_SELECT.options.remove(0);
}

function loadTexts() {
    texts.forEach(t => {
        // replace hyphens with spaces and prepend the path and extension
        // so the logic below need not be changed if format changes
        TEXT_SELECT.add(new Option(t.replaceAll('-', ' '), "../texts/" + t + ".html"))
    });
}

function loadFontTexts(fontFamily) {
    if (fontFamily === '')
        return;

    // TODO: this does not work, it filters out everything
    Object.entries(fontTexts).filter((k, v) => fontFamily.toString().startsWith(k)).forEach((k, v) => {
        TEXT_SELECT.add(new Option(k + '/' + v.replaceAll('-', ' '), "../fontTexts/" + v + ".html"))
    });
}

function getFont() {
    return CONTENT.style.fontFamily;
}


function setFont(font) {
    CONTENT.style.fontFamily = font;

    TEXT_SELECT.disabled = false;
}

function setFontFamily(fontFamily) {
    fontFamilies[fontFamily].forEach(fonts => {
        FONT_STYLE_SELECT.add(new Option(fonts[0].toString().replace(/([A-Z])/g, ' $1').trim(), fonts[1]))
    });

    FONT_STYLE_SELECT.disabled = false;

    clearTexts();
    loadFontTexts(fontFamily);
    loadTexts();
}

function btnEnable(value) {
    const font = FONT_STYLE_SELECT.selectedOptions[0].value;
    if (font === '')
        return;

    if (value === true) {
        setFont(FONT_STYLE_SELECT.selectedOptions[0].value);
    } else {
        setFont('');
    }
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

// document.addEventListener('DOMContentLoaded', e => {
//     let params = new URLSearchParams(location.search);
//     const intro = params.get('intro')
//     setFont(intro);
//
//     // swap to default
//     lastFont = '';
//
//     // this is the intro so dont allow changing text
//     TEXT_SELECT.disabled = true;
//     TEXT_SELECT.add(new Option('Introduction', '', true, true))
//
//     params.get('name') # => "n1"
//     params.getAll('name') # => ["n1", "n2"]
// });

FONT_STYLE_SELECT.disabled = true;
TEXT_SELECT.disabled = true;

fetch('../data.json')
    .then((response) => response.json())
    .then((json) => {
        fontFamilies = json['fonts'];
        texts = json['texts'];
        fontTexts = json['fontTexts'];

        Object.keys(fontFamilies).forEach(f => FONT_FAMILY_SELECT.add(new Option(f.replace(/([A-Z])/g, ' $1').trim(), f)));
    })
    .catch(e => {
        if (e != null)
            console.error('Error fetching data.json ', e);
    });

// document.addEventListener('DOMContentLoaded', e => {
// }
