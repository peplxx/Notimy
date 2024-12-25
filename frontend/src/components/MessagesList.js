import styles from './MessagesList.module.css';
import {useEffect, useRef} from "react";
import {useAutoAnimate} from "@formkit/auto-animate/react";
import classNames from "classnames";

const MessagesList = ({messages, isOpen, order_id, bottom=0 , children}) => {
    const listEnd = useRef();

    const [parent] = useAutoAnimate()

    // Для Анимации выезда сообщений
    useEffect(() => {
        if (isOpen) {
            messages.forEach((message, index) => {
                setTimeout(() => {
                    const messageElement = document.getElementById(`order-${order_id}-message-${index}`);
                    if (messageElement) {
                        messageElement.classList.remove(styles.disappear);
                        messageElement.classList.add(styles.appear);
                    }
                }, 50 * index); // 0.1s задержка между появлениями
            });
        } else if (!isOpen) {
            messages.forEach((message, index) => {
                setTimeout(() => {
                    const messageElement = document.getElementById(`order-${order_id}-message-${index}`);
                    if (messageElement) {
                        messageElement.classList.remove(styles.appear);
                        messageElement.classList.add(styles.disappear);
                    }
                }, 30); // 0.1s задержка между появлениями
            });
        }
    }, [isOpen, messages]);

    return (
        <div className={styles.messages} ref={parent} style={{bottom: bottom}}>
            {messages.map((message, index) => (
                <div
                    key={index}
                    id={`order-${order_id}-message-${index}`}
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