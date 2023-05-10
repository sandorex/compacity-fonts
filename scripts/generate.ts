// this script generates data about fonts available and paths to them so they
// don't have to be added manually

import * as fs from 'fs';
import * as path from 'path'

const rootDir = path.join(__dirname, '..');
const fontsDir = path.join(rootDir, 'fonts');
const textsDir = path.join(rootDir, 'texts');
const fontTextsDir = path.join(rootDir, 'fontTexts');
const outDir = rootDir;

function listDir(dir: string): { files: string[], dirs: string[] } {
    let files: string[] = [];
    let dirs: string[] = [];

    try {
        for (const file of fs.readdirSync(dir)) {
            const stat = fs.statSync(path.join(dir, file));
            if (stat.isFile())
                files.push(file);
            else if (stat.isDirectory())
                dirs.push(file);
        }
    } catch(e) {
        console.error("Error listing files in " + dir, e);
        return { files: [], dirs: [] };
    }

    return { files: files, dirs: dirs };
}

(async () => {
    let data: {
        fonts: string[];
        texts: string[];
        fontTexts: Record<string, string[]>;
    } = {} as any;

    data.fonts = [];
    data.texts = [];
    data.fontTexts = {};

    // generate css file that includes all the fonts and list of all fonts
    let css = '';
    listDir(fontsDir).files.forEach(f => {
        const name = path.parse(f).name;

        css += `@font-face {
    font-family: '$font';
    src: url(fonts/$path);
    font-weight: normal;
    font-style: normal;
}

`.replace('$font', name).replace('$path', f);
        data.fonts.push(name);
    });

    // write a css file that includes all the fonts
    fs.writeFile(path.join(outDir, 'fonts.css'), css, (err: any) => {
        if (err)
            console.error("Error writing to file", err);
    });

    // find all texts files but remove extension as all of them should be html
    data.texts = listDir(textsDir).files.map(f => path.parse(f).name);

    // find all font specific texts
    listDir(fontTextsDir).dirs.forEach(d => {
        data.fontTexts[d] = listDir(path.join(fontTextsDir, d)).files.map(f => path.parse(f).name);
    });

    // write all the data in easy readable JSON file
    fs.writeFile(path.join(outDir, 'data.json'), JSON.stringify(data), (err: any) => {
        if (err) {
            console.error("Error writing to file", err);
        }
    });
})();

