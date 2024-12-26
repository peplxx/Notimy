import styles from "components/OrderBottom.module.css";
import React from "react";
import {QuickMessages} from "./QuickMessages";

export const InputMessage = ({newMessage, setNewMessage, sendMessage, inputRef}) => {

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
                ref={inputRef}
                className={styles.messageInput}
                placeholder="Введите сообщение"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onClick={(e) => e.stopPropagation()}
                onKeyDown={handleKeyDown}
            />
            <div
                className={styles.sendBtn}
                onClick={send}
            >
                    <img src="/svg/Vector.svg" className={styles.sendBtnIcon} />
            </div>
            <QuickMessages setNewMessage={setNewMessage} inputRef={inputRef}/>
        </div>
    )
}