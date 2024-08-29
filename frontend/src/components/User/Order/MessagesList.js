import styles from './MessagesList.module.css';
import {useContext, useEffect, useRef, useState} from "react";
import OrderContext from "../../../context/OrderContext";
import {useAutoAnimate} from "@formkit/auto-animate/react";
import classNames from "classnames";

const MessagesList = ({children}) => {
    const {messages, isOpen, order} = useContext(OrderContext);
    const listEnd = useRef();

    const [parent] = useAutoAnimate()
    useEffect(() => {
        if (listEnd.current && isOpen) {
            listEnd.current.scrollIntoView({behavior: "smooth"});
        }
    }, [messages, isOpen]);

    useEffect(() => {
        if (isOpen) {
            messages.forEach((message, index) => {
                setTimeout(() => {
                    const messageElement = document.getElementById(`order-${order.id}-message-${index}`);
                    if (messageElement) {
                        messageElement.classList.remove(styles.disappear);
                        messageElement.classList.add(styles.appear);
                    }
                }, 30 * (messages.size - index <= 4 ? 4 - messages.size + index : 0)); // 0.1s задержка между появлениями
            });
        } else if (!isOpen) {
            messages.forEach((message, index) => {
                setTimeout(() => {
                    const messageElement = document.getElementById(`order-${order.id}-message-${index}`);
                    if (messageElement) {
                        messageElement.classList.remove(styles.appear);
                        messageElement.classList.add(styles.disappear);
                    }
                }, 30); // 0.1s задержка между появлениями
            });
        }
    }, [isOpen]);
    return (
        <div className={styles.messages} ref={parent}>
            {messages.length === 0 ? (
                <div
                    key="0"
                    id={`order-${order.id}-message-default`}
                    className={classNames(styles.message)}
                >
                    Ваш заказ принят в обработку
                </div>
            ) : null}
            {messages.map((message, index) => (
                <div
                    key={index}
                    id={`order-${order.id}-message-${index}`}
                    className={classNames(styles.message, styles.disappear)}
                >
                    {message.text}
                </div>
            ))}
            {children}
            <div ref={listEnd}/>
        </div>
    )
}

export default MessagesList;