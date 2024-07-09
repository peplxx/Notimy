import React, { useState, useEffect } from 'react';
import axiosBase from "../../config/axios";
import styles from './OrderList.module.css';
import Order from '../Order/Order';

interface OrderData {
    id: number;
    title: string;
    description: string;
    color: string;
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
    }, []);

    return (
        <div className={styles.order_list}>
            {orders.map(order => (
                <Order
                    key={order.id}
                    title={order.title}
                    description={order.description}
                    color={order.color}
                />
            ))}
        </div>
    );
};

export default OrderList;
