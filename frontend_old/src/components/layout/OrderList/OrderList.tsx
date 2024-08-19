// frontend_old/src/components/layout/OrderList/OrderList.tsx
import React from 'react';
import styles from './OrderList.module.css';
import Order from '@/components/ui/Order/Order';
import { useOrders } from '@/components/hooks/OrdersContext';

const OrderList: React.FC = () => {
    const { orders, deleteOrder } = useOrders();

    return (
        <div className={styles.order_list}>
            {orders.map(order => (
                <Order
                    key={order.id}
                    closed_at={order.closed_at}
                    code={order.code}
                    provider_name={order.providerName}
                    id={order.id}
                    onDelete={() => deleteOrder(order.id)}
                />
            ))}
        </div>
    );
};

export default OrderList;
