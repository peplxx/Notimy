import React, {useContext} from 'react';
import Order from 'components/Admin/Order/Order';
import AdminContext from 'context/AdminContext';
import {AdminOrderProvider} from "context/AdminOrderContext";

import styles from './OrderList.module.css';
import {useAutoAnimate} from "@formkit/auto-animate/react";

const OrderList = ({orders, children}) => {
    const [parent] = useAutoAnimate()
    console.log(orders);
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
