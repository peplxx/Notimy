import styles from './MessagesList.module.css';
import {useContext, useEffect, useRef, useState} from "react";
import OrderContext from "../../../context/OrderContext";
import {useAutoAnimate} from "@formkit/auto-animate/react";

const MessagesList = ({children}) => {
    const {messages, isOpen} = useContext(OrderContext);
    const listEnd = useRef();

    const [parent] = useAutoAnimate()
    useEffect(() => {
        if (listEnd.current && isOpen) {
            listEnd.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, isOpen]);

    return (
        <div className={styles.messages} ref={parent}>
            {messages.map((message) => (
                <div className={styles.message} >
                    {message.text}
                </div>
            ))}
            {children}
            <div ref={listEnd} />
        </div>
    )
}

export default MessagesList;