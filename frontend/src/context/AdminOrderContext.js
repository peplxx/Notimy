import React, {createContext, useState, useContext, useEffect} from 'react';
import getBackground from 'utils/gradientById';
import AdminContext from "./AdminContext";
import {closeOrderApiAdmin} from "../utils/api";
import sleep from "utils/sleep";

const AdminOrderContext = createContext();


export const AdminOrderProvider = ({children, InitOrder}) => {
    const {
        deleteOrder: deleteOrderContext,
        closeOrder: closeOrderContext,
        sendMessage
    } = useContext(AdminContext);
    const [order, setOrder] = useState(InitOrder); // Данные О Заказе
    const [isOpen, setIsOpen] = useState(false); // Открытие/Закрытие Заказа
    const [isDeleting, setIsDeleting] = useState(false); // Процесс Удаления
    const [isReady, setIsReady] = useState(false); // Статус Заказа
    const [backgroundStyles, setBackgroundStyles] = useState(null);
    const [isSideOpen, setIsSideOpen] = useState(false); // Открытие/Закрытие Слайдера
    const [newMessage, setNewMessage] = useState('');
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

    useEffect(() => {
        setIsReady(order.status);
        setBackgroundStyles(getBackground(order.id, false));
    }, [order]);

    useEffect(() => {
        if (isReady) {
            setBackgroundStyles({background: `gray`});
        }
    }, [isReady]);

    return (
        <AdminOrderContext.Provider
            value={{
                order, setOrder, isOpen, setIsOpen, isDeleting,
                deleteOrder, isReady, closeOrder, backgroundStyles, isSideOpen, setIsSideOpen,
                newMessage, setNewMessage, sendMessage
            }}>
            {children}
        </AdminOrderContext.Provider>
    );
};

export default AdminOrderContext;
