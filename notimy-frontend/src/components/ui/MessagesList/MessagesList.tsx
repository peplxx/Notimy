import styles from "./MessagesList.module.css";
import React from "react";


const MessagesList: React.FC = () => {
    return (
        <div className={styles.messages}>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
            <div className={styles.message}>asd</div>
        </div>
    )
}

export default MessagesList;