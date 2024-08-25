import styles from './MessagesList.module.css';
import {useContext, useEffect, useRef} from "react";
import {useAutoAnimate} from "@formkit/auto-animate/react";
import AdminOrderContext from "context/AdminOrderContext";

const MessagesList = ({children}) => {
    const {messages, isOpen} = useContext(AdminOrderContext);
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