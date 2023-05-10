'use strict';

// const storedTheme = localStorage.getItem('theme')
const toggleBtn = document.getElementById('theme-toggle');
const iconLight = toggleBtn.children[0];
const iconDark = toggleBtn.children[1];

function getPreferedTheme() {
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme !== null)
        return storedTheme;

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function getCurrentTheme() {
    return document.documentElement.getAttribute('data-bs-theme');
}

function setTheme(value) {
    if (value === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')

        iconLight.style.display = 'inline';
        iconDark.style.display = 'none';

        localStorage.setItem("theme", 'dark');
    } else {
        document.documentElement.setAttribute('data-bs-theme', value)

        if (value == 'dark') {
            iconLight.style.display = 'inline';
            iconDark.style.display = 'none';
        } else {
            iconLight.style.display = 'none';
            iconDark.style.display = 'inline';
        }

        localStorage.setItem("theme", value);
    }
}

function toggleTheme() {
    const theme = getCurrentTheme();
    if (theme == 'light')
        setTheme('dark');
    else if (theme == 'dark')
        setTheme('light');
    else
        // default to dark
        setTheme('dark');
}

document.addEventListener('DOMContentLoaded', (e) => {
    // set saved or preferred theme
    setTheme(getPreferedTheme());
})
