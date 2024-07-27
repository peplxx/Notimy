import React, {useState} from 'react';
import AdminOrderFooter from './Footer/AdminOrderFooter';
import AdminOrderTop from './Top/AdminOrderTop';
import styles from './AdminOrder.module.css';
import classNames from 'classnames';

import CryptoJS from 'crypto-js';

interface Props {
    title: string;
    id: string;
}

const Order: React.FC<Props> = ({title, id}) => {
    const [isOpen, setIsOpen] = useState(false);
    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

    const hash: string = CryptoJS.MD5(id).toString(CryptoJS.enc.Hex);
    const hashNumber: number = parseInt(hash, 16) % 360;


    let mainHue1 = ((hashNumber) % 360);
    if (mainHue1 < 150) mainHue1 += mainHue1 / 150 * 50;
    let mainHue2 = ((mainHue1 + 100) % 360);
    let backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${mainHue2}, 71%, 79%, 1) 10%, hsla(${mainHue1}, 70%, 81%, 1) 60%)`
    };

    if (title == 'BAZZAR') {
        // Зеленый градиент (оттенки зелёного цвета)
        const greenHue2 = (hashNumber % 40) + 100; // Диапазон 90-150
        const greenHue1 = ((hashNumber + 30) % 60) + 90;

        backgroundStyle = {
            background: `linear-gradient(345deg, hsla(${greenHue2}, 70%, 85%, 1) 10%, hsla(${greenHue1}, 70%, 70%, 1) 60%)`
        };
    }


    return (
        <div
            className={classNames(styles.order, {
                [styles.orderClosed]: !isOpen,
                [styles.orderOpened]: isOpen,
            })}
            onClick={toggleOrder}
        >
            <AdminOrderTop title={title} backgroundStyle={backgroundStyle}/>
            <AdminOrderFooter backgroundStyle={backgroundStyle}/>
        </div>
    );
};

export default Order;
