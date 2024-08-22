import React, {createContext, useState, useEffect, useCallback} from 'react';
import {createChannelAdmin, deleteOrderApiUser, fetchOrdersAdmin, sendMessageAdmin} from 'utils/api';

const AdminContext = createContext();

export const AdminProvider = ({children}) => {
    const [orders, setOrders] = useState([]);

    const fetchOrders = useCallback(async () => {
        try {
            const orders = await fetchOrdersAdmin();
            setOrders(orders);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    useEffect(()=>{
        fetchOrders();
    }, []);

    const createChannel = async () => {
        const response = await createChannelAdmin();
        if ( response ) {
            await fetchOrders();
        } else {
            //TODO show error;
        }
    }

    const sendMessage = async(id, message) => {
        if ( await sendMessageAdmin(id, message) ) {
            await fetchOrders();
        }
    }

    const deleteOrder = async (id) => {
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

    return (
        <AdminContext.Provider value={{orders, createChannel, deleteOrder, sendMessage}}>
            {children}
        </AdminContext.Provider>
    );
};

export default AdminContext;
