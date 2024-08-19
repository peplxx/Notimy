import React, {useContext} from "react";
import classNames from "classnames";

import MessagesList from "components/Admin/Order/MessagesList";
import AdminOrderContext from "context/AdminOrderContext";

import styles from './OrderBottom.module.css';

const OrderBottom = () => {
    const {order, backgroundStyles}= useContext(AdminOrderContext);

    return (
    <div className={classNames(styles.bottom)} style={backgroundStyles}>
        <MessagesList messages={order.messages} />
        <div className={styles.datetime}>{order.closed_at}</div>
        <div className={styles.toggleBtn}>...</div>
    </div>
    );
};

export default OrderBottom;