import React, { useState, useEffect, ReactNode } from 'react';
import axiosBase from "@/utils/axios"; // using the alias for imports
import styles from './OrderList.module.css';
import Order from '@/components/ui/Order/Order'; // using the alias for imports

interface OrderData {
    id: string;
    title: string;
}

interface OrderListProps {
    children: ReactNode;
}


const OrderList: React.FC<OrderListProps> = ({children}) => {
    const [orders, setOrders] = useState<OrderData[]>([]);

    // useEffect(() => {
    //     const fetchOrders = async () => {
    //         try {
    //             const response = await axiosBase.get('/test_orders');
    //             setOrders(response.data);
    //         } catch (error) {
    //             console.error('Error fetching orders:', error);
    //         }
    //     };
    //
    //     fetchOrders();
    //     const interval = setInterval(fetchOrders, 1000);
    //
    //     return () => clearInterval(interval);
    // }, []);

    return (
        <div className={styles.order_list}>
            {children}
            {orders.map(order => (
                <Order
                    key={order.id}
                    title={order.title}
                    id={order.id}
                />
            ))}
        </div>
    );
};

export default OrderList;
