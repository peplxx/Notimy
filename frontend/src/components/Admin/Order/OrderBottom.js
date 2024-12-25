import React, {useRef, useState} from "react";
import {styled} from "styled-components";

import MessagesList from "components//MessagesList";
import {InputMessage} from "./InputMessage";
import {formatDate} from "utils/formatDate";
import {QuickMessages} from "../../QuickMessages";

import styles from './OrderBottom.module.css';

const OrderBottomStyled = styled.div`
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100%;
    background-color: #2ecc71;
    border-radius: inherit;
    z-index: -10;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-start;
    box-shadow: ${(props) => (props.isOpen ? 'inset 0 0 10em rgba(0, 0, 0, 0.3)' : 'none')};
    transition: box-shadow 0.5s ease-in-out;
    ${(props) => props.backgroundStyles};
`;


const OrderBottom = ({order_id, messages_data, creatated_at, backgroundStyles, isOpen, sendMessage}) => {
    // Компнент нижней части заказа
    // Получает на вход props:
    //  - айди заказа
    //  - Список сообещний
    //  - Стили для цвета
    //  - Состояние открыт или закрыт
    //  - Функцию отправки сообщения
    //  - Дату создания заказа
    // Содержит:
    //  - список сообщений заказ
    //  - Инпут для сообщения, кнопку отрпавить, заготовленные сообщение

    const [newMessage, setNewMessage] = useState("");
    // Добавляем референс для инпута
    const inputRef = useRef(null);


    return (
        <OrderBottomStyled isOpen={isOpen} backgroundStyles={backgroundStyles} >
            <MessagesList messages={messages_data} isOpen={isOpen} order_id={order_id} bottom="1.1em"/>

            <QuickMessages setNewMessage={setNewMessage} inputRef={inputRef}/>
            <InputMessage newMessage={newMessage} setNewMessage={setNewMessage} sendMessage={sendMessage} inputRef={inputRef} />

            <div className={styles.datetime}>{creatated_at}</div>
            <div className={styles.toggleBtn}>...</div>
             {/*<div className={styles.code}>код заказа: {order.code}</div>*/}
        </OrderBottomStyled>
    );
};

export default OrderBottom;