import styles from "./MessagesList.module.css";
import React, { ReactNode } from "react";


interface MessageListProps {
    messages: string[];
    children: ReactNode;
}

const MessagesList: React.FC<MessageListProps> = ({messages=[], children}) => {
    return (
        <div className={styles.messages}>
            {messages.map((message) => (
                <div className={styles.message}>{message}</div>
            ))}
            {children}
        </div>
    )
}

export default MessagesList;