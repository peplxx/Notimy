import React, {useContext, useEffect} from 'react';
import classNames from "classnames";

import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';
import OrderContext from "context/OrderContext";

import styles from './Order.module.css';

const Order = () => {
    const {setIsOpen, isOpen, isDeleting} = useContext(OrderContext);
    
    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className={
            classNames(
                styles.order,
                isOpen ? styles.orderOpened : styles.orderClosed,
                isDeleting ? styles.orderShaking : null
            )}
             onClick={toggleOrder}
        >
            <OrderTop/>
            <OrderBottom/>
        </div>
    );
};

export default Order;
