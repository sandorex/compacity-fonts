import * as fs from 'fs';
import * as path from 'path'

const rootDir = path.join(__dirname, '..');
const fontsDir = path.join(rootDir, 'fonts');
const textsDir = path.join(rootDir, 'texts');
const fontTextsDir = path.join(rootDir, 'fontTexts');
const outDir = rootDir;

// convenience function that returns list of files and directories in a dir
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
    // find all fonts and make css to include them all
    const fontFiles = listDir(fontsDir).files.reverse();

    let fonts: Record<string, [string, string][]> = {};
    let css = '';
    fontFiles.forEach(f => {
        const name = path.parse(f).name;
        let [family, style] = name.split('-');

        css += `@font-face{font-family: '$font';src: url(fonts/$path);font-weight: normal;font-style: normal;}
`.replace('$font', name).replace('$path', f);

        if (fonts[family] === undefined)
            fonts[family] = [];

        if (style === undefined)
            style = 'Normal';

        fonts[family].push([style, name]);
    });

    fs.writeFile(path.join(outDir, 'fonts.css'), css, (err: any) => {
        if (err)
            console.error("Error writing to file", err);
    });

    // get all the texts
    let texts: string[] = [];
    listDir(textsDir).files.forEach(f => texts.push(path.parse(f).name));

    // get all the font specific texts
    let fontTexts: Record<string, string[]> = {};
    listDir(fontTextsDir).dirs.forEach(d => {
        fontTexts[d] = listDir(path.join(fontTextsDir, d)).files.map(f => path.parse(f).name);
    });

    // map the data
    const data = {
        fonts: fonts,
        texts: texts,
        fontTexts: fontTexts,
    };

    // save as easy to read json
    fs.writeFile(path.join(outDir, 'data.json'), JSON.stringify(data), (err: any) => {
        if (err)
            console.error("Error writing to file", err);
    });
})();

