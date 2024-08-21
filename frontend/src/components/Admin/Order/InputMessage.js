import styles from "./OrderBottom.module.css";
import React from "react";

export const InputMessage = ({message, setMessage, sendMessage}) => {

     const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            sendMessage(e);
        }
    };

    return (
        <div className={styles.inputMessage}>
            <input
                className={styles.messageInput}
                placeholder="Введите сообщение"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onClick={(e) => e.stopPropagation()}
                onKeyDown={handleKeyDown}
            />
            <button
                className={styles.sendBtn}
                onClick={(e) => {sendMessage(e)}}
            >
                &gt;
            </button>
        </div>
    )
}