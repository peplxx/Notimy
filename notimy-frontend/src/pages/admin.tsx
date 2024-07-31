// pages/admin.tsx
import React, { useState, useCallback, useEffect } from "react";
import Header from '../components/layout/Header/Header';
import AdminAddBtn from "../components/ui/AdminAddBtn/AdminAddBtn";
import styles from '../assets/styles/global.module.css';
import OrderList from "../components/layout/OrderList/OrderList";
import AdminOrder from "@/components/ui/AdminOrder/AdminOrder";
import axiosInstance from "@/utils/axios";

interface OrderData {
    id: string;
    title: string;
}

function Admin() {
    // List of orders data.
    const [orders, setOrders] = useState<OrderData[]>([]);

    // Update orders data.
    const fetchOrders = useCallback(async () => {
        try {
            const response = await axiosInstance.get('/update_orders');
            setOrders(response.data);
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }, []);

    // 
    useEffect(() => {
        fetchOrders();
        const interval = setInterval(fetchOrders, 10000);

        return () => clearInterval(interval);
    }, [fetchOrders]);

    // Add order and update list.
    const addOrder = async () => {
        try {
            await axiosInstance.post('/add-order');
            fetchOrders(); // Refresh the list of orders after adding a new one
        } catch (error) {
            console.error('Error adding order:', error);
        }
    };

    return (
        <div className={styles.App}>
            <div className={styles.Background}/>
            <Header/>
            <OrderList orders={orders}>
                <AdminAddBtn onAddOrder={addOrder}/>
                <AdminOrder title={"asd"} id={"123"} />
            </OrderList>
        </div>
    );
}

export default Admin;
