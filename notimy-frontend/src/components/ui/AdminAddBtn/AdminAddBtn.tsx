import React, { useState, useEffect } from 'react';
// import OrderFooter from './Footer/OrderFooter';
import OrderTop from '../Order/Top/OrderTop';
import styles from '../Order/Order.module.css';
import classNames from 'classnames';
import stylesHeader from './Top/OrderTop.module.css';
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
            className={classNames(styles.order)}
            onClick={toggleOrder}
        >
            <OrderTop title={title} backgroundStyle={backgroundStyle} />
            {/*<OrderFooter backgroundStyle={backgroundStyle} />*/}
        </div>
    );
};

export default Order;
