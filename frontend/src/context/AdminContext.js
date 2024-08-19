import React, {createContext, useState, useEffect, useCallback} from 'react';
import {createChannelAdmin, deleteOrderApi, getMeAdmin} from 'utils/api';

const AdminContext = createContext();

export const AdminProvider = ({children}) => {
    const [orders, setOrders] = useState([]);

    const getMe = useCallback(async () => {
        try {
            const me = await getMeAdmin();
            console.log(me);
            setOrders(me.orders);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    useEffect(()=>{
        getMe();
    }, []);

    const createChannel = async () => {
        const response = await createChannelAdmin();
        if ( response ) {
            getMe();
        } else {
            //TODO show error;
        }
    }

    const deleteOrder = async (id) => {
        const timeDeleteStart = Date.now();
        if (await deleteOrderApi(id)) {
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
