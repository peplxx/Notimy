import styles from "./MessagesList.module.css";
import React, { ReactNode } from "react";


interface MessageListProps {
    children: ReactNode;
}

const MessagesList: React.FC<MessageListProps> = ({children}) => {
    return (
        <div className={styles.messages}>
            <div className={styles.message}>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias, aliquam explicabo? Accusamus adipisci animi architecto beatae, corporis eaque error exercitationem illo libero nihil obcaecati quo reiciendis repellendus? Accusantium, ducimus itaque!</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            {children}
        </div>
    )
}

export default MessagesList;