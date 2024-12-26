import React, {useContext, useEffect, useState} from 'react';
import Order from 'components/User/Order/Order';
import UserContext from '../../context/UserContext';
import {OrderProvider} from "context/OrderContext";

import styles from './OrderList.module.css';
import {useAutoAnimate} from "@formkit/auto-animate/react";

const OrderList = ({orders, admin=false, children}) => {
    const [parent] = useAutoAnimate()
    const [readyOrderCount, setReadyOrderCount] = useState(1000);

    useEffect(() => {
        // Подсчет текущего количества готовых заказов
        const currentReadyOrderCount = orders.filter(order => !order.open).length;

        // Если текущее количество готовых заказов больше предыдущего, воспроизвести звук
        if (currentReadyOrderCount > readyOrderCount) {
            console.log('done')
            const audio = new Audio('/ready.mp3');
            try {
                audio.play()
            } catch (e) {
                console.log(e)
            }
        }

        // Обновление состояния с количеством готовых заказов
        setReadyOrderCount(currentReadyOrderCount);
    }, [orders]);

    return (
        <div className={styles.order_list} ref={parent}>
            {children}
            {orders.map(order => (
                <Order key={`order-${order.id}`} admin={admin} />
                // <OrderProvider key={`OrderProviderFor${order.id}`} InitOrder={order}>
                // </OrderProvider>
            ))}
        </div>
    );
};

export default OrderList;

