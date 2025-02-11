import React, {createContext, useState, useCallback, useEffect} from 'react';
import {
    closeOrderApiAdmin,
    createChannelAdmin,
    deleteOrderApiUser,
    fetchOrdersAdmin, getMeSpot,
    sendMessageAdmin
} from 'utils/api';
import styles from "components/Admin/Order/OrderTop.module.css";

const AdminContext = createContext();

export const AdminProvider = ({children}) => {
    // Context который только взаимодействует с api и информацией о админе (список заказов)
    const [orders, setOrders] = useState([]);
    const [spot, setSpot] = useState('...');
    const [qrCode, setQrCode] = useState(null);

    const updateOrders = useCallback(async () => {
        try {
            const fetchedOrders = await fetchOrdersAdmin();
            const sortedOrders = fetchedOrders.channels_data.sort((a, b) =>
                new Date(b.created_at) - new Date(a.created_at)
            );
            setSpot(fetchedOrders.provider_name || "Касса");
            setOrders([...sortedOrders]);
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
        if ( message === '' ) {
            return;
        }
        if (  await sendMessageAdmin(id, message)) {
            await updateOrders();
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

    const closeOrder = async (id) => {
        return await closeOrderApiAdmin(id);
    }

    return (
        <AdminContext.Provider value={{orders, createOrder, deleteOrder, sendMessage, closeOrder, setQrCode}}>
            <div style={{width: "100%", position: "absolute", display: "flex", justifyContent: "center"}}>
                <span style={{
                    position: "absolute",
                    // left: "calc(50%)",
                    top: ".2em",
                    color: "white",
                    fontWeight: 700,
                    fontSize: "2em"
                }}>
                    {spot}
                </span>
            </div>
            {qrCode !== null ? (
                <> 
                <div className={styles.qrCode} onClick={(e) => { setQrCode(null); e.stopPropagation(); }}>
                    {qrCode}
                </div>
                <div className={styles.darkBackground}></div>
                </>

            ) : null}
                {children}
        </AdminContext.Provider>
);
};

export default AdminContext;
