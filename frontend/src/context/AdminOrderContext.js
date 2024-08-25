import React, {createContext, useState, useContext, useEffect} from 'react';
import getBackground from 'utils/gradientById';
import AdminContext from "./AdminContext";
import {closeOrderApiAdmin, sendMessageAdmin} from "../utils/api";
import sleep from "utils/sleep";

const AdminOrderContext = createContext();


export const AdminOrderProvider = ({children, InitOrder}) => {
    const {
        deleteOrder: deleteOrderContext,
        closeOrder: closeOrderContext,
        sendMessage: sendMessageContext
    } = useContext(AdminContext);
    const [order, setOrder] = useState(InitOrder); // Данные О Заказе
    const [isOpen, setIsOpen] = useState(false); // Открытие/Закрытие Заказа
    const [isDeleting, setIsDeleting] = useState(false); // Процесс Удаления
    const [isReady, setIsReady] = useState(false); // Статус Заказа
    const [backgroundStyles, setBackgroundStyles] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isSideOpen, setIsSideOpen] = useState(false); // Открытие/Закрытие Слайдера
    const [newMessage, setNewMessage] = useState('');
    useEffect(() => {
        setOrder(InitOrder)
    }, [InitOrder]);

    useEffect(() => {
        if (messages.length !== order.messages_data.length) {
            setMessages(order.messages_data);
            console.log(messages)
        }
    }, [order, messages]);


    const closeOrder = async () => {
        const res = await closeOrderContext(order.id);
        await sleep(200);
        setIsReady(res);
        return res;
    }

    const deleteOrder = async () => {
        setIsDeleting(true);
        const result = await deleteOrderContext(order.id);
        setIsDeleting(result);
        return result;
    }

    const sendMessage = async (message) => {
        await sendMessageContext(order.id, message);

    }

    useEffect(() => {
        if (messages.length !== order.messages_data.length) {
            setMessages(order.messages_data);
        }
    }, [order, messages]);


    useEffect(() => {
        setIsReady(!order.open);
    }, [order]);

    useEffect(() => {
        if (isReady) {
            setBackgroundStyles({background: `gray`});
        } else {
            setBackgroundStyles(getBackground(order.id, false));
        }
    }, [isReady, order]);

    return (
        <AdminOrderContext.Provider
            value={{
                order, setOrder, isOpen, setIsOpen, isDeleting,
                deleteOrder, isReady, closeOrder, backgroundStyles, isSideOpen, setIsSideOpen,
                newMessage, setNewMessage, sendMessage, messages
            }}>
            {children}
        </AdminOrderContext.Provider>
    );
};

export default AdminOrderContext;
