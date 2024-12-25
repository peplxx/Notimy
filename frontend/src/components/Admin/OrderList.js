import React from 'react';
import Order from 'components/Admin/Order/Order';

import styles from './OrderList.module.css';
import {useAutoAnimate} from "@formkit/auto-animate/react";

const OrderList = ({orders, children}) => {
    const [parent] = useAutoAnimate()

    return (
        <div className={styles.order_list} ref={parent}>
            {children}
            {orders.map(order => (
                <Order key={`Order${order.id}`} order={order} />
            ))}
        </div>
    );
};

export default OrderList;
