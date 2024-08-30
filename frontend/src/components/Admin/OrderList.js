import React, {useContext} from 'react';
import Order from 'components/Admin/Order/Order';
import AdminContext from 'context/AdminContext';
import {AdminOrderProvider} from "context/AdminOrderContext";

import styles from './OrderList.module.css';
import {useAutoAnimate} from "@formkit/auto-animate/react";

const OrderList = ({children}) => {
    const {orders} = useContext(AdminContext);
    const [parent] = useAutoAnimate()

    return (
        <div className={styles.order_list} ref={parent}>
            {children}
            {orders.map(order => (
                <AdminOrderProvider key={`OrderProvider${order.id}`} InitOrder={order}>
                    <Order key={`Order${order.id}`}/>
                </AdminOrderProvider>
            ))}
        </div>
    );
};

export default OrderList;
