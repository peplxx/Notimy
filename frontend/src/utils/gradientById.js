import CryptoJS from "crypto-js";

export default function backgroundStyleByIdAndStatus(id, status) {

    const hash = CryptoJS.SHA256(id).toString(CryptoJS.enc.Hex);
    const hash2 = CryptoJS.MD5(id.slice(0, 13)).toString(CryptoJS.enc.Hex);
    const hashNumber = parseInt(hash, 16) % 360;
    const hashNumber2 = parseInt(hash2, 16) % 360;

    let mainHue1 = ((hashNumber) % 360);
    // if (mainHue1 < 150) mainHue1 += mainHue1 / 150 * 50;
    // let mainHue2 = ((mainHue1 + 100) % 360);

    let mainHue2 = ((hashNumber2) % 360);

    if (Math.abs(mainHue2 - mainHue1) <= 30 ) mainHue2 = (mainHue2 + 100) % 360

    let backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${mainHue2}, 71%, 79%, 1) 10%, hsla(${mainHue1}, 70%, 81%, 1) 60%)`
    };
    if (status) {
        const greenHue2 = 120; // (hashNumber % 40) + 100;
        const greenHue1 = 130; //((hashNumber + 30) % 60) + 90;

        backgroundStyle = {
            background: `linear-gradient(345deg, hsla(${greenHue2}, 70%, 95%, 1) 10%, hsla(${greenHue1}, 70%, 80%, 1) 60%)`
        };
    }
    return backgroundStyle
}
