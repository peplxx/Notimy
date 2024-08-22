import styles from './MessagesList.module.css';

const MessagesList = ({messages, children}) => {
    return (
        <div className={styles.messages}>
            {messages.map((message) => (
                <div className={styles.message}>
                    {message.text}
                </div>
            ))}
            {children}
        </div>
    )
}

export default MessagesList;