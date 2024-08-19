// frontend_old/src/components/hooks/OrdersContext.tsx
import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import axiosInstance from '@/utils/axiosInstance';

interface Order {
    id: string;
    providerName: string;
    code: string;
    closed_at: string;
}

interface OrdersContextType {
    orders: Order[];
    deleteOrder: (id: string) => void;
}

const OrdersContext = createContext<OrdersContextType | undefined>(undefined);

export const OrdersProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [orders, setOrders] = useState<Order[]>([{id:"1234", providerName:"BAZZAR", code:"NU5G3", closed_at:"01.01.2000 | 15:10"}]);

    // Кидает Запрос На /me И Обновляет Состояние Заказов
    const fetchOrders = useCallback(async () => {
        try {
            const response = await axiosInstance.get('/me', { withCredentials: true });
            const channels = response.data['channels'];
            const ordersData = channels.map((order: any) => ({
                id: order.id,
                providerName: order['provider-name'],
                code: order.code,
                closed_at: order.closed_at,
            }));
            setOrders(ordersData);
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }, []);

    // Убирает Заказ Из Списка
    const deleteOrder = (id: string) => {
        setOrders(prevOrders => prevOrders.filter(order => order.id !== id));
    };

    // Брать Заказы каждые 10 секунд
    useEffect(() => {
        fetchOrders();
        const interval = setInterval(fetchOrders, 10000);
        return () => clearInterval(interval);
    }, [fetchOrders]);

    return (
        <OrdersContext.Provider value={{ orders, deleteOrder }}>
            {children}
        </OrdersContext.Provider>
    );
};

export const useOrders = () => {
    const context = useContext(OrdersContext);
    if (!context) {
        throw new Error('useOrders must be used within an OrdersProvider');
    }
    return context;
};

