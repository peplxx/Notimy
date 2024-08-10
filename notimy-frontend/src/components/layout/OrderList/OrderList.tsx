// components/layout/OrderList/OrderList.tsx
import React, { ReactNode } from 'react';
import styles from './OrderList.module.css';
import Order from '@/components/ui/Order/Order'; // using the alias for imports

interface OrderData {
    id: string;
    providerName: string;
    code: string;
    closed_at: string;
}

interface OrderListProps {
    orders: OrderData[];
    // children: ReactNode;
}

const OrderList: React.FC<OrderListProps> = ({ orders }) => {
    console.log("ORDERLIST: " + orders);
    return (
        <div className={styles.order_list}>
            {orders.map(order => (
                <Order
                    closed_at={order.closed_at}
                    code={order.code}
                    provider_name={order.providerName}
                    id={order.id}
                />
            ))}
            {/*{children}*/}
        </div>
    );
};


export default OrderList;
