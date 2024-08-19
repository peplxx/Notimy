import React, {useContext} from "react";
import classNames from "classnames";

import MessagesList from "components/User/Order/MessagesList";
import OrderContext from "context/OrderContext";

import styles from './OrderBottom.module.css';

const OrderBottom = () => {
    const {order, backgroundColorStyles}= useContext(OrderContext);

    return (
    <div className={classNames(styles.bottom)} style={backgroundColorStyles}>
        <MessagesList messages={order.messages} />
        <div className={styles.datetime}>{order.closed_at}</div>
        <div className={styles.toggleBtn}>...</div>
    </div>
    );
};

export default OrderBottom;