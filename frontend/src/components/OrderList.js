import React, {useEffect, useState} from 'react';
import {styled} from "styled-components";
import {useAutoAnimate} from "@formkit/auto-animate/react";

import Order from 'components/Order';

const OrderListStyled = styled.div`
    position: relative;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 100%;
    max-width: var(--mainMaxWidth);
`

const OrderList = ({orders, admin=false, children}) => {
    const [parent] = useAutoAnimate()
    console.log(orders)
    const [readyOrderCount, setReadyOrderCount] = useState(1000);

    useEffect(() => {
        // Подсчет текущего количества готовых заказов
        const currentReadyOrderCount = orders.filter(order => !order.open).length;

        // Если текущее количество готовых заказов больше предыдущего, воспроизвести звук
        if (!admin && currentReadyOrderCount > readyOrderCount) {
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
        <OrderListStyled ref={parent}>
            {children}
            {orders.map(order => (
                <Order key={`Order${order.id}`} order={order} admin={admin}/>
            ))}
        </OrderListStyled>
    );
};

export default OrderList;
