import React, {useContext} from 'react';
import classNames from "classnames";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';
import AdminOrderContext from "context/AdminOrderContext";

import styles from './Order.module.css';

const Order = () => {
    const {setIsOpen, isOpen, isDeleting} = useContext(AdminOrderContext);

    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

  return (
    <div className={
        classNames(
            styles.order,
            isOpen ? styles.orderOpened : styles.orderClosed,
            isDeleting ? styles.orderSlidingOut : null
        )}
         onClick={toggleOrder}>
      <OrderTop />
      <OrderBottom />
    </div>
  );
};

export default Order;
