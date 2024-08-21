// src/context/UserContext.js
import React, {createContext, useState, useEffect, useCallback} from 'react';
import {deleteOrderApiUser, fetchOrders, joinChannel} from 'utils/api';

const UserContext = createContext();

export const UserProvider = ({children}) => {
    const [orders, setOrders] = useState([]);

    // Function to load orders from the API
    const loadOrders = useCallback(async () => {
        try {
            const fetchedOrders = await fetchOrders();
            setOrders(fetchedOrders);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    // Fetch orders initially and set up polling every 10 seconds
    useEffect(() => {
        loadOrders();
        const interval = setInterval(loadOrders, 10000);
        return () => clearInterval(interval);
    }, [loadOrders]);


    const addOrder = async (id) => {
        const newOrder = await joinChannel(id);
        setOrders((prevOrders) => [...prevOrders, newOrder]);
    };

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
        <UserContext.Provider value={{orders, addOrder, deleteOrder}}>
            {children}
        </UserContext.Provider>
    );
};

export default UserContext;
