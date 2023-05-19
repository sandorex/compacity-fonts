'use strict';

// globals //
const CONTENT = document.getElementById('content');
const FONT_SELECT = document.getElementById('font-select');
const TEXT_SELECT = document.getElementById('text-select');
const ENABLE_BTN = document.getElementById('btn-check-enable');
const ROOT = document.querySelector(':root');

// stores last selected font family
let lastFontFamily = '';

// functions //
function isEnabled() { return ENABLE_BTN.checked; }

// inserts spaces before capital letters to format things properly
function insertSpaces(x) {
   return x.toString().replace(/([A-Z])/g, ' $1').trim();
}

function setMemes(value) {
    if (value)
        CONTENT.textContent = ''; // clear content

    // hide / show all the memes
    Array.from(document.getElementsByClassName('meme')).forEach(e => {
        if (value)
            e.classList.remove('hidden');
        else
            e.classList.add('hidden');
    })
}

function clearContent() {
    CONTENT.textContent = '';
}

function resetTextSelection() {
    clearContent();
    TEXT_SELECT.selectedIndex = 0;

    setMemes(true);
}

// handlers //
function handleBoldToggle(value) {
    if (value === true)
        CONTENT.style.fontWeight = 'bold';
    else
        CONTENT.style.fontWeight = '';
}

function handleItalicsToggle(value) {
    if (value === true)
        CONTENT.style.fontStyle = 'italic';
    else
        CONTENT.style.fontStyle = '';
}

function handleEnableToggle(value) {
    const font = FONT_SELECT.selectedOptions[0].value;

    // ignore invalid options
    if (!font)
        return;

    if (value === true)
        CONTENT.style.fontFamily = font;
    else
        CONTENT.style.fontFamily = '';
}

function handleSelectText(option) {
    const value = option.value;

    if (!value)
        return;

    fetch(option.value)
        .then(response => response.text())
        .then(data => {
            // clear the children
            clearContent();

            // insert new content
            CONTENT.innerHTML = data;

            setMemes(false);
        });
}

function handleSelectFont(_) {
    const fontOpt = FONT_SELECT.selectedOptions[0];
    const font = fontOpt.value;
    const fontFamily = fontOpt.dataset.fontFamily;

    // set it globally so it can be used freely
    ROOT.style.setProperty('--font-selected', font);

    if (isEnabled())
        handleEnableToggle(true);

    if (lastFontFamily !== fontFamily) {
        lastFontFamily = fontFamily;

        Array.from(TEXT_SELECT.getElementsByTagName('option')).forEach(opt => {
            if (opt.dataset.fontFamily !== undefined)
                opt.hidden = opt.dataset.fontFamily !== fontFamily;
        });

        // reset if the text is hidden now
        if (TEXT_SELECT.selectedOptions[0].hidden)
            resetTextSelection();
    }

    TEXT_SELECT.disabled = false;
}

// initialization //
TEXT_SELECT.disabled = true;

fetch('data.json')
    .then((response) => response.json())
    .then((json) => {
        const fontFamilies = json['fonts'];
        const texts = json['texts'];
        const fontTexts = json['fontTexts'];

        // add all fontTexts but hidden and with their own groups
        Object.keys(fontTexts).forEach(family => {
            fontTexts[family].forEach(text => {
                var opt = new Option(text.toString().replace('-', ' '), 'fontTexts/' + family + '/' + text + '.html');
                opt.dataset.fontFamily = family;
                opt.hidden = true;

                TEXT_SELECT.add(opt);
            });
        });

        texts.forEach(text => TEXT_SELECT.add(new Option(text.replaceAll('-', ' '), "texts/" + text + ".html")));

        // group up the variants by the family
        Object.keys(fontFamilies).forEach(family => {
            var group = document.createElement('optgroup');
            group.label = insertSpaces(family);

            fontFamilies[family].forEach(variant => {
                var opt = new Option(variant[0], variant[1]);
                opt.dataset.fontFamily = family;

                group.appendChild(opt);
            });

            FONT_SELECT.add(group);
        });
    })
    .catch(e => {
        if (e != null)
            console.error('Error fetching data.json ', e);
    });
