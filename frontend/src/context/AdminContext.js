import React, {createContext, useState, useEffect, useCallback} from 'react';
import {createChannelAdmin, deleteOrderApiAdmin, fetchOrdersAdmin} from 'utils/api';

const AdminContext = createContext();

export const AdminProvider = ({children}) => {
    const [orders, setOrders] = useState([]);

    const fetchOrders = useCallback(async () => {
        try {
            const orders = await fetchOrdersAdmin();
            console.log(orders);
            setOrders(orders);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    useEffect(()=>{
        fetchOrdersAdmin();
    }, []);

    const createChannel = async () => {
        const response = await createChannelAdmin();
        if ( response ) {
            await fetchOrders();
        } else {
            //TODO show error;
        }
    }

    const deleteOrder = async (id) => {
        const timeDeleteStart = Date.now();
        if (await deleteOrderApiAdmin(id)) {
            const timeDeleteEnd = Date.now();
            const timeToSleep = Math.max(0, 900 - (timeDeleteEnd - timeDeleteStart));
            await new Promise(resolve => setTimeout(resolve, timeToSleep));
            setOrders(prevOrders => prevOrders.filter(order => order.id !== id));
            return true;
        }
        return false;
    }

    return (
        <AdminContext.Provider value={{orders, createChannel, deleteOrder}}>
            {children}
        </AdminContext.Provider>
    );
};

export default AdminContext;
