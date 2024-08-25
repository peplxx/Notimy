import React, {createContext, useState, useEffect, useCallback} from 'react';
import {
    closeOrderApiAdmin,
    createChannelAdmin,
    deleteOrderApiUser,
    fetchOrdersAdmin,
    sendMessageAdmin
} from 'utils/api';

const AdminContext = createContext();

export const AdminProvider = ({children}) => {
    // Context который только взаимодействует с api и информацией о админе (список заказов)
    const [orders, setOrders] = useState([]);

    const updateOrders = useCallback(async () => {
        try {
            const fetchedOrders = await fetchOrdersAdmin();
            console.log('update');
            setOrders([...fetchedOrders]);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    useEffect(() => {
        updateOrders();
    }, []);

    const createOrder = async () => {
        const response = await createChannelAdmin();
        if (response) {
            await updateOrders();
        } else {
            console.error("Failed to create order")
        }
    }

    const sendMessage = async (id, message) => {
        if (await sendMessageAdmin(id, message)) {
            await updateOrders();
        }
    }

    const deleteOrder = async (id) => {
        // TODO убрать таймеры, только слать запрос
        const timeDeleteStart = Date.now();
        if (await deleteOrderApiUser(id)) {
            const timeDeleteEnd = Date.now();
            const timeToSleep = Math.max(0, 900 - (timeDeleteEnd - timeDeleteStart));
            await new Promise(resolve => setTimeout(resolve, timeToSleep));
            setOrders(prevOrders => prevOrders.filter(order => order.id !== id));
            return true;
        }
        return false;
    }

    const closeOrder = async (id) => {
        return await closeOrderApiAdmin(id);
    }

    return (
        <AdminContext.Provider value={{orders, createOrder, deleteOrder, sendMessage, closeOrder}}>
            {children}
        </AdminContext.Provider>
    );
};

export default AdminContext;
