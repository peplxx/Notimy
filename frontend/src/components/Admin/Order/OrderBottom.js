import React, {useContext, useState} from "react";
import classNames from "classnames";

import MessagesList from "components/Admin/Order/MessagesList";
import AdminOrderContext from "context/AdminOrderContext";

import styles from './OrderBottom.module.css';
import {InputMessage} from "./InputMessage";
import AdminContext from "../../../context/AdminContext";
import {sendMessageAdmin} from "../../../utils/api";

const OrderBottom = () => {
    const {order, backgroundStyles} = useContext(AdminOrderContext);
    const { sendMessage: sendMessageApi } = useContext(AdminContext);
    const [message, setMessage] = useState("");

    const sendMessage = () => {
        sendMessageApi(order.id, message);
        setMessage("");
        return true;
    }

    return (
        <div className={classNames(styles.bottom)} style={backgroundStyles}>
            <MessagesList messages={order.messages_data}>
                <InputMessage message={message} setMessage={setMessage} sendMessage={sendMessage}/>
            </MessagesList>
            <div className={styles.datetime}>{order.created_at}</div>
            <div className={styles.toggleBtn}>...</div>
        </div>
    );
};

export default OrderBottom;