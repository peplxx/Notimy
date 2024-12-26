import React, {useContext, useState} from 'react';
import classNames from "classnames";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';

import styles from './Order.module.css';
import {formatDate} from "utils/formatDate";
import backgroundStyleByIdAndStatus from "utils/gradientById";
import {AppContext} from "context/App";

const Order = ({order, admin = false}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isSideOpen, setIsSideOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isQrOpen, setIsQrOpen] = useState(false);
    const [qrCode, setQrCode] = useState("");
    const backgroundStyles = backgroundStyleByIdAndStatus(order.id, order.status)

    const {sendMessage, closeOrder: closeOrderCall, deleteOrder: deleteOrderCall} = useContext(AppContext);

    async function deleteOrder() {
        setIsDeleting(true);
        await deleteOrderCall(order.id);
        setIsDeleting(false);
        setIsSideOpen(false);
    }

    async function closeOrder() {
        await closeOrderCall(order.id);
        setIsSideOpen(false)
    }

    return (
        <div className={
            classNames(
                styles.order,
                isOpen ? styles.orderOpened : styles.orderClosed,
                isDeleting ? styles.orderShaking : null
            )}
        >
            {/*{admin && <>*/}
                <OrderTop order={order}
                          backgroundStyles={backgroundStyles}
                          isReady={!order.open}
                          isSideOpen={isSideOpen}
                          setIsSideOpen={setIsSideOpen}
                          setIsOpen={setIsOpen}
                          closeOrder={() => closeOrder(order.id)}
                          deleteOrder={() => deleteOrder(order.id)}
                          isOpen={isOpen}
                          isQrOpen={isQrOpen} // TODO fix qr code open
                          setIsQrOpen={setIsQrOpen}
                          setQrCode={setQrCode}
                          admin={admin}
                />
                <OrderBottom
                    order_id={order.id}
                    messages_data={order.messages_data}
                    created_at={formatDate(order.created_at)}
                    admin={admin}
                    backgroundStyles={backgroundStyles}
                    isOpen={isOpen}
                    sendMessage={(message) => sendMessage(order.id, message)} // TODO fix this func
                />
            {/*</>*/}
            {/*}*/}
        </div>
    );
};

export default Order;
