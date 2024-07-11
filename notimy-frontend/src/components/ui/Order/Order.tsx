import React, { useState, useEffect } from 'react';
import OrderFooter from '../OrderFooter';
import OrderTop from '../OrderTop';
import styles from './Order.module.css';
import classNames from 'classnames';
import stylesHeader from './OrderHeader.module.css';
import stylesFooter from './OrderFooter.module.css';

import CryptoJS from 'crypto-js';

interface Props {
    title: string;
    description: string;
    id: string;
}

const Order: React.FC<Props> = ({ title, description, id }) => {
    const [isOpen, setIsOpen] = useState(false);
    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

    const hash: string = CryptoJS.MD5(id).toString(CryptoJS.enc.Hex);
    const hashNumber: number = parseInt(hash, 16) % 360;

    const backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${hashNumber}, 71%, 79%, 1) 0%, hsla(${(hashNumber+100)%360}, 70%, 81%, 1) 60%);`
    }

    return (
        <div
            className={classNames(styles.order, {
                [styles.orderClosed]: !isOpen,
                [styles.orderOpened]: isOpen,
            })}
            onClick={toggleOrder}
        >
            <OrderTop title={title} backgroundStyle={backgroundStyle} />
            <OrderFooter backgroundStyle={backgroundStyle} />
        </div>
    );
};

export default Order;
