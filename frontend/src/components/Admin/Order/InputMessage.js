import styles from "./OrderBottom.module.css";
import React, {useContext} from "react";
import AdminOrderContext from "context/AdminOrderContext";

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
                <img src="/svg/Vector.svg" style={{width: ".8em",position: "absolute", top: ".55em", left: ".55em"}}/>
            </div>
        </div>
    )
}