// src/components/OrderList.js
import React, { useContext } from 'react';
import Order from 'components/User/Order/Order';
import UserContext from '../../context/UserContext';
import {OrderProvider} from "context/OrderContext";

import styles from './OrderList.module.css';

const OrderList = () => {
  const { orders } = useContext(UserContext);

  return (
    <div className={styles.order_list}>
      {orders.map(order => (
          <OrderProvider key={order.id} InitOrder={order}>
            <Order />
          </OrderProvider>
      ))}
    </div>
  );
};

export default OrderList;
