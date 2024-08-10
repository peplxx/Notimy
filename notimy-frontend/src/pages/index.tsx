import React, {createContext, useCallback, useEffect, useState} from 'react';
import Header from '../components/layout/Header/Header';
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css';
import Order from '@/components/ui/Order/Order';
import axiosInstance from '@/utils/axiosInstance';


interface OrderData {
    id: string;
    providerName: string;
    code: string;
    closed_at: string;
}

interface OrdersContextProps {
    orders: OrderData[];
    deleteOrder: (orderId: string) -> void;
}

const OrdersContext = createContext<OrdersContextProps | undefined>(undefined);


function App() {


    // List of orders data.
    const [orders, setOrders] = useState<OrderData[]>([]);

    const fetchOrders = useCallback(async () => {
    try {
        const response = await axiosInstance.get('/me', { withCredentials: true });
        console.log(response.data);

        const channels = response.data['channels'];
        const ordersData: OrderData[] = channels.map(order => ({
            id: order.id,
            providerName: order['provider-name'], // Using bracket notation to access 'provider-name'
            code: order.code,
            closed_at: order.closed_at
        }));
        console.log(ordersData);
        setOrders(ordersData); // Update the state with the fetched orders
        console.log("orders: " + orders);
    } catch (error) {
        console.error('Error fetching orders:', error);
    }
}, []); // Empty dependency array to mimic componentDidMount (runs once)


    // 
    useEffect(() => {
        fetchOrders();
        const interval = setInterval(fetchOrders, 10000);

        return () => clearInterval(interval);
    }, [fetchOrders]);


    return (
        <div className={styles.App}>
            {/*<Header/>*/}
            <OrderList orders={orders}>
                {/*<Order title={"1"} id={"1"}/>*/}
                {/*<Order title={"2"} id={"2"}/>*/}
                {/*<Order title={"3"} id={"3"}/>*/}
                {/*<Order title={"4"} id={"4"}/>*/}
                {/* {null} */}
            </OrderList>
            
        </div>
    );
}

export default App;
