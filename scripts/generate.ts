import * as fs from 'fs';
import * as path from 'path'

const rootDir = path.join(__dirname, '..');
const fontsDir = path.join(rootDir, 'fonts');
const textsDir = path.join(rootDir, 'texts');
const outDir = rootDir;

const cssTemplate = `@font-face {
    font-family: '$font';
    src: url(fonts/$path);
    font-weight: normal;
    font-style: normal;
}

`;

(async () => {
    let data: Record<string, any> = {};

    // generate css file that includes all the fonts and list of all fonts
    try {
        let css = '';
        const files = await fs.promises.readdir(fontsDir);

        let fonts: Array<string> = [];
        for (const file of files) {
            const fileName = path.parse(file).name;
            const filePath = path.join(fontsDir, file);

            const stat = await fs.promises.stat(filePath);
            if (!stat.isFile())
                continue;

            css += cssTemplate.replace('$font', fileName).replace('$path', file);
            fonts.push(fileName);
        }

        data['fonts'] = fonts;
        fs.writeFile(path.join(outDir, 'fonts.css'), css, (err: any) => {
            if (err) {
                console.error("Error writing to file", err);
            }
        });
    } catch(e) {
        console.error("Error iterating over font files", e);
    }

    // iterate over texts and gather a list of them
    try {
        const files = await fs.promises.readdir(textsDir);

        let texts: Array<string> = [];
        for (const file of files) {
            const fileName = path.parse(file).name;

            const stat = await fs.promises.stat(path.join(textsDir, file));
            if (!stat.isFile())
                continue;

            texts.push(fileName);
        }

        data['texts'] = texts;
    } catch(e) {
        console.error("Error iterating over texts", e);
    }

    fs.writeFile(path.join(outDir, 'data.json'), JSON.stringify(data), (err: any) => {
        if (err) {
            console.error("Error writing to file", err);
        }
    });
})();

