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
import {FaApple} from "react-icons/fa";
import {styled} from "styled-components";

const TgAlertStyled = styled.div`
    position: fixed;
    bottom: 1rem;
    left: 1rem;
    padding: 0.5rem;

    font-size: 0.75rem;

    border-radius: 0.5rem;
    border: .1em #404040 solid;
    color: white;
    box-shadow: 0 .3em .9em black;
`

function MainApp() {
    // Че я хочу
    // Чтобы здесь были данные
    // О юзере, статус, заказы
    // user = {status: 'admin'/'user'/'anon'}
    // orders = [order1, order2, ...]

    const {me, isIOS} = useAuth();
    const [user_status, setUserStatus] = useState('anon');
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        if (me) {
            setUserStatus(me.role);
            setOrders(me.channels_data.sort((a, b) =>
                new Date(b.created_at) - new Date(a.created_at)
            ))
            console.log(orders)
        }
    }, [me])


    async function deleteOrder(id) {
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

    async function closeOrder(id) {
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
        }}>
            <>
                {user_status === 'user' && <UserApp orders={orders}/>}
                {user_status === 'spot_user' && <AdminApp orders={orders}/>}
                {user_status === 'user' &&
                    isIOS &&
                    !me.tg &&
                    <a href={`https://t.me/NotimyAppBot?start=uuid=${me.id}`}>
                        <TgAlertStyled>
                            <FaApple /> Уведомления отключены на iOS.<br />
                            Авторизуйтесь через Telegram,<br />
                            чтобы их включить.<br />
                            Нажмите здесь.
                        </TgAlertStyled>
                    </a>}
            </>
        </AppContext.Provider>
    );
}

export default MainApp;
