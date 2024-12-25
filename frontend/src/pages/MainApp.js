import React, {useCallback, useContext, useEffect, useState} from "react";
import {AppContext} from "../context/App";
import AdminApp from "./AdminApp";
import UserApp from "./UserApp";
import {useAuth} from "../utils/auth";
import {createChannelAdmin, deleteOrderApiUser, fetchOrdersAdmin} from "../utils/api";

function MainApp() {
    // Че я хочу
    // Чтобы здесь были данные
    // О юзере, статус, заказы
    // user = {status: 'admin'/'user'/'anon'}
    // orders = [order1, order2, ...]

    const {me} = useAuth();
    const [status, setStatus] = useState('anon');
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        if ( me ) {
            setStatus(me.role);
            setOrders(me.orders);
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
            status,
            orders,
            deleteOrder,
            createOrder
        }} >
            <>
                {status === 'user' && <UserApp orders={orders}/>}
                {status === 'spot_user' && <AdminApp orders={orders}/>}
            </>
        </AppContext.Provider>
    );
}

export default MainApp;
