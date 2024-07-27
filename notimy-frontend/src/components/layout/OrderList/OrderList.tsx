// components/layout/OrderList/OrderList.tsx
import React, { ReactNode } from 'react';
import styles from './OrderList.module.css';
import Order from '@/components/ui/Order/Order'; // using the alias for imports

interface OrderData {
    id: string;
    title: string;
}

interface OrderListProps {
    orders: OrderData[];
    children: ReactNode;
}

const OrderList: React.FC<OrderListProps> = ({ orders, children }) => {
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
