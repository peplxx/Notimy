import React, {useContext} from 'react';
import Order from 'components/Admin/Order/Order';
import AdminContext from 'context/AdminContext';
import {AdminOrderProvider} from "context/AdminOrderContext";

import styles from './OrderList.module.css';

const OrderList = ({children}) => {
    const {orders} = useContext(AdminContext);
    console.log(orders)
    return (
        <div className={styles.order_list}>
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
