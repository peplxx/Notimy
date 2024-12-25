import React, {useContext, useState} from 'react';
import classNames from "classnames";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';
import AdminOrderContext from "context/AdminOrderContext";

import styles from './Order.module.css';
import OrderContext from "../../../context/OrderContext";

const Order = ({order}) => {
    const {isOpen} = useState(false);
    const {isDeleting} = useState(false);
    const {setIsQrOpen} = useState(false);
    const {isQrOpen} = useState(false);

    return (
        <div className={
            classNames(
                styles.order,
                isOpen ? styles.orderOpened : styles.orderClosed,
                isDeleting ? styles.orderShaking : null
            )}
        >

            <OrderTop order={order}
            backgroundStyles={{}}
            isReady={false}
            isSideOpen={false}
            setIsSideOpen={false}
            setIsOpen={false}
            isOpen={false}
            isQrOpen={false}
            setIsQrOpen={false}
            deleteOrder={false}
                      closeOrder={0}
                      setQrCode={0}/>
            <OrderBottom
                order={order}
                backgroundStyles={0}
                isOpen={0}
                sendMessage={0}
                sendMessageApi={0}
                newMessage={0}
                setNewMessage={0}
            />
        </div>
    );
};

export default Order;
