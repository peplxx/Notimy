import React, { useState, useRef, useEffect } from "react";
import MessagesList from "../../MessagesList/MessagesList";

import styles from "../AdminOrder.module.css";
import stylesFooter from "./AdminOrderFooter.module.css";

interface Props {
    backgroundStyle: React.CSSProperties;
}

const AdminOrderFooter: React.FC<Props> = ({ backgroundStyle }) => {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState<string[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    };

    const sendMessage = (e?: React.MouseEvent<HTMLButtonElement> | React.KeyboardEvent<HTMLInputElement>) => {
        if (e) e.stopPropagation();
        if (message.trim() !== "") {
            setMessages([...messages, message]);
            setMessage("");
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            sendMessage(e);
        }
    };

    return (
        <div className={styles.footer} style={backgroundStyle}>
            <MessagesList messages={messages}>
                <div className={stylesFooter.inputMessage}>
                    <input
                        className={stylesFooter.messageInput}
                        placeholder="Введите сообщение"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onClick={(e) => e.stopPropagation()}
                        onKeyDown={handleKeyDown}
                    />
                    <button
                        className={stylesFooter.sendBtn}
                        onClick={(e) => sendMessage(e)}
                    >
                        &gt;
                    </button>
                </div>
                <div ref={messagesEndRef} />
            </MessagesList>
            <div className={styles.date}>08.07.2024 | 20:08</div>
            <div className={stylesFooter.toggleBtn}>...</div>
        </div>
    );
};

export default AdminOrderFooter;
