const path = require('path');
const fs = require('fs');

console.log('\nRunning pre-build tasks');

var appVersion;

try {
    appVersion = require('../../package.json').version;
} catch {
    console.warn('Could not import package.json.');
    appVersion = undefined;
}

const versionFilePath = path.join(
    __dirname + '/../src/environments/version.ts'
);
const src = `export const version = '${appVersion}';
`;

// ensure version module pulls value from package.json
fs.writeFile(versionFilePath, src, { flat: 'w' }, function (err) {
    if (err) {
        return console.log(err);
    }

    console.log(`Updating application version ${appVersion}`);
    console.log(`${'Writing version module to '}${versionFilePath}\n`);
    console.log(src);
});
