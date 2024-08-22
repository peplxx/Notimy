import React, {useContext} from "react";
import classNames from "classnames";

import MessagesList from "components/User/Order/MessagesList";
import OrderContext from "context/OrderContext";

import styles from './OrderBottom.module.css';
import {formatDate} from "../../../utils/formatDate";

const OrderBottom = () => {
    const {order, backgroundColorStyles, isOpen} = useContext(OrderContext);

    return (
        <div
            className={classNames(styles.bottom)}
            style={{
                ...backgroundColorStyles,
                boxShadow: !isOpen ? 'inset 0 0 10em rgba(0, 0, 0, 0.3)' : 'none',
                transition: 'box-shadow .5s ease-in-out'
            }}
        >
            <MessagesList messages={order.messages_data}/>
            <div className={styles.datetime}>{ formatDate( order.created_at) }</div>
            <div className={styles.toggleBtn}>...</div>
        </div>
    );
};

export default OrderBottom;