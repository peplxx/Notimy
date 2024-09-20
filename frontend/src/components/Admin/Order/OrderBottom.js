import React, {useContext, useRef, useState} from "react";
import classNames from "classnames";
import MessagesList from "components//MessagesList";
import AdminOrderContext from "context/AdminOrderContext";
import styles from './OrderBottom.module.css';
import {InputMessage} from "./InputMessage";
import AdminContext from "context/AdminContext";
import {formatDate} from "utils/formatDate";

// Predefined quick messages
const QUICK_MESSAGES = [
    "Ваш заказ готов!",
    "Ваш заказ принят!",
    "Ваш заказ будет готов через  мин.",
    "Ваш заказ задерживается на  мин."
];

const OrderBottom = () => {
    const {order, backgroundStyles, isOpen} = useContext(AdminOrderContext);
    const {sendMessage: sendMessageApi} = useContext(AdminContext);
    const {newMessage, setNewMessage, sendMessage} = useContext(AdminOrderContext);
    const [showQuickMessages, setShowQuickMessages] = useState(false);
    const inputRef = useRef(null); // Добавляем реф для инпута

    const toggleQuickMessages = () => {
        setShowQuickMessages(!showQuickMessages);
    };

    const onQuickMessageClick = (message) => {
        const position = message.indexOf(" мин.");

        if (position !== -1) {
            // Если в сообщении есть фраза "...на ", добавляем текст и устанавливаем курсор
            setNewMessage(`${message}`);

            // Для установки курсора после текста "...на ":
            setTimeout(() => {
                const cursorPosition = position;
                inputRef.current.focus();
                inputRef.current.setSelectionRange(cursorPosition, cursorPosition);
            }, 0);
        } else {
            // Для остальных сообщений просто добавляем их в инпут
            setNewMessage(message);
        }

        toggleQuickMessages();
    };

    return (

        <div
            className={classNames(styles.bottom)}
            style={{
                ...backgroundStyles,
                boxShadow: !isOpen ? 'inset 0 0 10em rgba(0, 0, 0, 0.3)' : 'none',
                transition: 'box-shadow .5s ease-in-out'
            }}
        >
            <MessagesList messages={order.messages_data} isOpen={isOpen} order={order} bottom="1.1em"/>

            {/* Toggle button for quick messages */}
            <div className={styles.toggleQuickMessages} onClick={toggleQuickMessages}>
                <img src='/svg/Group.svg' style={{width: ".8em", position: "absolute", top: ".8em", left: ".4em"}}/>
            </div>

            {/* Quick messages popup */}
            {showQuickMessages && (
                <div className={styles.quickMessagesPopup}>
                    {QUICK_MESSAGES.map((quickMessage, index) => (
                        <div
                            key={index}
                            className={styles.quickMessage}
                            onClick={() => onQuickMessageClick(quickMessage)}
                        >
                            {quickMessage}
                        </div>
                    ))}
                </div>
            )}

            {/* Добавляем реф к компоненту InputMessage */}
            <InputMessage inputRef={inputRef} />
            <div className={styles.datetime}>{formatDate(order.created_at)}</div>
            <div className={styles.toggleBtn}>...</div>
            <div className={styles.code}>код заказа: {order.code}</div>
        </div>
    );
};

export default OrderBottom;