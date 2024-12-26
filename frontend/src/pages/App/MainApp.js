import React, {useCallback, useEffect, useState} from "react";
import {AppContext} from "context/App";
import AdminApp from "pages/App/AdminApp";
import UserApp from "pages/App//UserApp";
import {useAuth} from "utils/auth";
import {
    closeOrderApiAdmin,
    createChannelAdmin,
    deleteOrderApiUser,
    fetchOrdersAdmin,
    sendMessageAdmin
} from "utils/api";

function MainApp() {
    // Че я хочу
    // Чтобы здесь были данные
    // О юзере, статус, заказы
    // user = {status: 'admin'/'user'/'anon'}
    // orders = [order1, order2, ...]

    const {me} = useAuth();
    const [user_status, setUserStatus] = useState('anon');
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        if ( me ) {
            setUserStatus(me.role);
            setOrders(me.channels_data.sort((a, b) =>
                new Date(b.created_at) - new Date(a.created_at)
            ))
            console.log(orders)
        }
    }, [me])


    async function deleteOrder (id) {
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

    const updateOrders = useCallback(async () => {
        try {
            const fetchedOrders = await fetchOrdersAdmin();
            const sortedOrders = fetchedOrders.channels_data.sort((a, b) =>
                new Date(b.created_at) - new Date(a.created_at)
            );
            // setSpot(fetchedOrders.provider_name || "Касса");
            setOrders([...sortedOrders]);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }, []);

    async function sendMessage(orderId, messageText) {
        await sendMessageAdmin(orderId, messageText)
        await updateOrders()
    }

    async function closeOrder (id) {
        await closeOrderApiAdmin(id);
        await updateOrders()
    }

    const createOrder = async () => {
        const response = await createChannelAdmin();
        if (response) {
            await updateOrders();
        } else {
            console.error("Failed to create order")
        }
    }

    return (
        <AppContext.Provider value={{
            me,
            user_status,
            orders,
            createOrder,
            closeOrder,
            deleteOrder,
            sendMessage
        }} >
            <>
                {user_status === 'user' && <UserApp orders={orders}/>}
                {user_status === 'spot_user' && <AdminApp orders={orders}/>}
            </>
        </AppContext.Provider>
    );
}

export default MainApp;
