import styles from "components/OrderBottom.module.css";
import React, {useState} from "react";
import {Popover, PopoverContent, PopoverTrigger} from "@nextui-org/popover";
import {MdAccountBox} from "react-icons/md";
import {formatDate} from "../../utils/formatDate";
import deleteSessionToken from "../../utils/deleteSessionToken";

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
            <Popover placement='top-end'>
                <PopoverTrigger>
                    <div className={styles.toggleQuickMessages} onClick={toggleQuickMessages}>
                        <img src='/svg/Group.svg' className={styles.quickMessageBtnIcon} />
                    </div>
                </PopoverTrigger>
                <PopoverContent>
                    <div className={styles.quickMessagesPopup}>
                        {QUICK_MESSAGES.map((quickMessage, index) => (<div
                            key={index}
                            className={styles.quickMessage}
                            onClick={() => onQuickMessageClick(quickMessage)}
                        >
                            {quickMessage}
                        </div>))}
                    </div>
                </PopoverContent>
            </Popover>

    </>)
}