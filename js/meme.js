'use strict';

// i do not want to plague the rest of logic with meme generating code.. lol
const MEME_IMG = document.getElementById('meme-img');
const MEME_LABEL = document.getElementById('meme-text');

let loadingMeme = false;

function memeGen() {
    if (loadingMeme)
        return;

    loadingMeme = true;

    // fetch a new meme
    fetch('https://meme-api.com/gimme')
        .then(response => response.json())
        .then(json => {
            // i do not want to get my website banned for dumb reason
            if (json['nsfw'] !== false)
                return;

            MEME_IMG.setAttribute('src', json['url']);
            MEME_LABEL.innerText = json.title;
        })
        .finally((_) => {
            // allow trying to load another even if it failed
            loadingMeme = false;
        });
}

MEME_IMG.addEventListener('mouseup', e => {
    if (e.shiftKey)
        memeGen();
});

