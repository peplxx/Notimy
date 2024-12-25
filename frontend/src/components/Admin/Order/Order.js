import React, {useContext, useState} from 'react';
import classNames from "classnames";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';
import AdminOrderContext from "context/AdminOrderContext";

import styles from './Order.module.css';
import OrderContext from "../../../context/OrderContext";
import {sendMessageAdmin} from "../../../utils/api";
import {formatDate} from "../../../utils/formatDate";

const Order = ({order}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isSideOpen, setIsSideOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isQrOpen, setIsQrOpen] = useState(false);
    const [qrCode, setQrCode] = useState("");

    return (
        <div className={
            classNames(
                styles.order,
                isOpen ? styles.orderOpened : styles.orderClosed,
                isDeleting ? styles.orderShaking : null
            )}
        >
            <OrderTop order={order}
                      backgroundStyles={{backgroundColor:'red'}}
                      isReady={false}
                      isSideOpen={isSideOpen}
                      setIsSideOpen={setIsSideOpen}
                      setIsOpen={setIsOpen}
                      isOpen={isOpen}
                      deleteOrder={() => {
                      }}
                      closeOrder={0}

                      isQrOpen={isQrOpen} // TODO fix qr code open
                      setIsQrOpen={setIsQrOpen}
                      setQrCode={setQrCode}
            />
            <OrderBottom
                order_id={order.id}
                messages_data={order.messages_data}
                creatated_at={formatDate(order.created_at)}
                backgroundStyles={0}
                isOpen={isOpen}
                sendMessage={sendMessageAdmin} // TODO fix this func
            />
        </div>
    );
};

export default Order;
