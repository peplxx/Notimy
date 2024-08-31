import styles from './MessagesList.module.css';
import {useContext, useEffect, useRef} from "react";
import {useAutoAnimate} from "@formkit/auto-animate/react";
import AdminOrderContext from "context/AdminOrderContext";
import classNames from "classnames";

const MessagesList = ({children}) => {
    const {messages, isOpen, order} = useContext(AdminOrderContext);
    const listEnd = useRef();

    const [parent] = useAutoAnimate()
    // useEffect(() => {
    //     if (listEnd.current && isOpen) {
    //         listEnd.current.scrollIntoView({behavior: "smooth"});
    //     }
    // }, [messages, isOpen]);

    useEffect(() => {
        if (isOpen) {
            messages.forEach((message, index) => {
                setTimeout(() => {
                    const messageElement = document.getElementById(`order-${order.id}-message-${index}`);
                    if (messageElement) {
                        messageElement.classList.remove(styles.disappear);
                        messageElement.classList.add(styles.appear);
                    }
                }, 50 * index); // 0.1s задержка между появлениями
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