import React, { useState, useEffect } from 'react';
import axiosBase from "../../../utils/axios";
import styles from './OrderList.module.css';
import Order from '../../ui/Order/Order';

interface OrderData {
    id: string;
    title: string;
}


const OrderList: React.FC = () => {
    const [orders, setOrders] = useState<OrderData[]>([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axiosBase.get('/test_orders');
                setOrders(response.data);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
        // Обновляем данные каждые 1 секунд
        const interval = setInterval(fetchOrders, 1000);

        // Чистим интервал при размонтировании компонента
        return () => clearInterval(interval);
    }, []);

    return (
        <div className={styles.order_list}>
            {orders.map(order => (
                <Order
                    title={order.title}
                    id={order.id}
                />
            ))}
        </div>
    );
};

export default OrderList;
