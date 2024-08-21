import React, {createContext, useState, useContext, useEffect} from 'react';
import getBackground from 'utils/gradientById';
import AdminContext from "./AdminContext";

const AdminOrderContext = createContext();


export const AdminOrderProvider = ({ children, InitOrder }) => {
    const {deleteOrder: deleteOrderContext} = useContext(AdminContext);
    const [order, setOrder] = useState(InitOrder); // Данные О Заказе
    const [isOpen, setIsOpen] = useState(false); // Открытие/Закрытие Заказа
    const [isDeleting, setIsDeleting] = useState(false); // Процесс Удаления
    const [isReady, setIsReady] = useState(false); // Статус Заказа
    const [backgroundStyles, setBackgroundStyles] = useState(null);
    const [isSideOpen, setIsSideOpen] = useState(false); // Открытие/Закрытие Слайдера
    async function closeOrder() {
        const sleep = ms => new Promise(r => setTimeout(r, ms));
        await sleep(1000);
        setIsReady(true);
        return true;
    }

    async function deleteOrder() {
        setIsDeleting(true);
        const result = await deleteOrderContext(order.id);
        setIsDeleting(result);
        return result;
    }

    const sendMessage = async () => {
        return true;
    }

    useEffect(() => {
        console.log(order.status)
        setIsReady(order.status);
        setBackgroundStyles( getBackground(order.id, false) );
    }, [order]);

    useEffect(() => {
        console.log(isReady)
        if ( isReady ) {
            console.log('change back');
            setBackgroundStyles( {background: `gray`} );
        }
    }, [isReady]);

    return (
        <AdminOrderContext.Provider
            value={{order, setOrder, isOpen, setIsOpen, isDeleting,
                deleteOrder, isReady, closeOrder, backgroundStyles, isSideOpen, setIsSideOpen}}>
            {children}
        </AdminOrderContext.Provider>
    );
};

export default AdminOrderContext;
