// src/components/OrderList.js
import React, {useContext, useEffect} from 'react';
import Order from 'components/User/Order/Order';
import UserContext from '../../context/UserContext';
import {OrderProvider} from "context/OrderContext";

import styles from './OrderList.module.css';
import {useAutoAnimate} from "@formkit/auto-animate/react";

const OrderList = ({children}) => {
    const {orders} = useContext(UserContext);
    const [parent] = useAutoAnimate()

    useEffect(()=>{
        // console.log(orders);
    },[orders]);

    return (
        <div className={styles.order_list} ref={parent}>
            {children}
            {orders.map(order => (
                <OrderProvider key={`OrderProviderFor${order.id}`} InitOrder={order}>
                    <Order key={`Order${order.id}`} />
                </OrderProvider>
            ))}
        </div>
    );
};

export default OrderList;
