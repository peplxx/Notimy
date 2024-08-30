import React, {useContext} from 'react';
import classNames from "classnames";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';
import AdminOrderContext from "context/AdminOrderContext";

import styles from './Order.module.css';

const Order = () => {
    const {isOpen, isDeleting} = useContext(AdminOrderContext);

    return (
        <div className={
            classNames(
                styles.order,
                isOpen ? styles.orderOpened : styles.orderClosed,
                isDeleting ? styles.orderShaking : null
            )}
        >
            <OrderTop/>
            <OrderBottom/>
        </div>
    );
};

export default Order;
