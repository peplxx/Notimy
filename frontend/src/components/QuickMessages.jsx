import styles from "./Admin/Order/OrderBottom.module.css";
import React, {useState} from "react";

// Predefined quick messages
const QUICK_MESSAGES = [
    "Ваш заказ готов!",
    "Ваш заказ принят!",
    "Ваш заказ будет готов через  мин.",
    "Ваш заказ задерживается на  мин."
];

export function QuickMessages({setNewMessage, inputRef}) {
    const [showQuickMessages, setShowQuickMessages] = useState(false);

    const toggleQuickMessages = () => {
        setShowQuickMessages(!showQuickMessages);
    };

    const onQuickMessageClick = (message) => {
        const position = message.indexOf(" мин.");

        if (position !== -1) {
            // Если в сообщении есть фраза " мин.", добавляем текст и устанавливаем курсор
            setNewMessage(`${message}`);

            // Для установки курсора после текста "...на ":
            setTimeout(() => {
                const cursorPosition = position;
                inputRef.current.focus();
                inputRef.current.setSelectionRange(cursorPosition, cursorPosition);
            }, 0);
        } else {
            // Для остальных сообщений просто добавляем их в инпут
            setNewMessage(message);
        }

        toggleQuickMessages();
    };

    return (<>
            <div className={styles.toggleQuickMessages} onClick={toggleQuickMessages}>
                <img src='/svg/Group.svg' style={{width: ".8em", position: "absolute", top: ".8em", left: ".4em"}}/>
            </div>
            {showQuickMessages && (<div className={styles.quickMessagesPopup}>
                {QUICK_MESSAGES.map((quickMessage, index) => (<div
                    key={index}
                    className={styles.quickMessage}
                    onClick={() => onQuickMessageClick(quickMessage)}
                >
                    {quickMessage}
                </div>))}
            </div>)}
        </>)
}