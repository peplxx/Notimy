export default function backgroundStyleByIdAndStatus(id, status) {

    const hash = Number(id); // CryptoJS.MD5(id).toString(CryptoJS.enc.Hex);
    const hashNumber = parseInt(hash, 16) % 360;

    let mainHue1 = ((hashNumber) % 360);
    if (mainHue1 < 150) mainHue1 += mainHue1 / 150 * 50;
    let mainHue2 = ((mainHue1 + 100) % 360);

    let backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${mainHue2}, 71%, 79%, 1) 10%, hsla(${mainHue1}, 70%, 81%, 1) 60%)`
    };
    if (status) {
        const greenHue2 = (hashNumber % 40) + 100;
        const greenHue1 = ((hashNumber + 30) % 60) + 90;

        backgroundStyle = {
            background: `linear-gradient(345deg, hsla(${greenHue2}, 70%, 85%, 1) 10%, hsla(${greenHue1}, 70%, 70%, 1) 60%)`
        };
    }
    return backgroundStyle
}
