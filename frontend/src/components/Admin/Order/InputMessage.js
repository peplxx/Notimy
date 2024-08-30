import styles from "./OrderBottom.module.css";
import React, {useContext} from "react";
import AdminOrderContext from "context/AdminOrderContext";

export const InputMessage = () => {

    const {newMessage, setNewMessage, sendMessage} = useContext(AdminOrderContext);

    const send = () => {
        sendMessage(newMessage);
        setNewMessage('');
    }

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            send();
        }
    };

    return (
        <div className={styles.inputMessage}>
            <input
                className={styles.messageInput}
                placeholder="Введите сообщение"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onClick={(e) => e.stopPropagation()}
                onKeyDown={handleKeyDown}
            />
            <button
                className={styles.sendBtn}
                onClick={send}
            >
                &gt;
            </button>
        </div>
    )
}