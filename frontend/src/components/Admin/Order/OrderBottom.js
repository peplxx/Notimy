import React, {useContext, useState} from "react";
import classNames from "classnames";

import MessagesList from "components/Admin/Order/MessagesList";
import AdminOrderContext from "context/AdminOrderContext";

import styles from './OrderBottom.module.css';
import {InputMessage} from "./InputMessage";
import AdminContext from "../../../context/AdminContext";
import {sendMessageAdmin} from "../../../utils/api";
import {formatDate} from "../../../utils/formatDate";

const OrderBottom = () => {
    const {order, backgroundStyles, isOpen} = useContext(AdminOrderContext);
    const {sendMessage: sendMessageApi} = useContext(AdminContext);
    const [message, setMessage] = useState("");

    const sendMessage = () => {
        sendMessageApi(order.id, message);
        setMessage("");
        return true;
    }

    return (
        <div
            className={classNames(styles.bottom)}
            style={{
                ...backgroundStyles,
                boxShadow: !isOpen ? 'inset 0 0 10em rgba(0, 0, 0, 0.3)' : 'none',
                transition: 'box-shadow .5s ease-in-out'
            }}
        >
            <MessagesList messages={order.messages_data}>
            </MessagesList>
            <InputMessage message={message} setMessage={setMessage} sendMessage={sendMessage}/>

            <div className={styles.datetime}>{formatDate(order.created_at)}</div>
            <div className={styles.toggleBtn}>...</div>
        </div>
    );
};

export default OrderBottom;