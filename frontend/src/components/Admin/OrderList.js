import React, { useContext } from 'react';
import Order from 'components/Admin/Order/Order';
import AdminContext  from 'context/AdminContext';
import {AdminOrderProvider} from "context/AdminOrderContext";

import styles from './OrderList.module.css';

const OrderList = () => {
  const { orders } = useContext(AdminContext);

  return (
    <div className={styles.order_list}>
      {orders.map(order => (
          <AdminOrderProvider key={order.id} InitOrder={order}>
            <Order />
          </AdminOrderProvider>
      ))}
    </div>
  );
};

export default OrderList;
