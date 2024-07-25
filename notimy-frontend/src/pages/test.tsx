import React from 'react';
import Header from '../components/layout/Header/Header';
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '@/assets/styles/global.module.css';
import AdminAddBtn from "../components/ui/AdminAddBtn/AdminAddBtn";
import Order from "@/components/ui/Order/Order";
// import Order from "../components/ui/Order/Order";

function Test() {
    return (
        <div className={styles.App}>
            <Header/>
            <AdminAddBtn/>
            <OrderList>
                <Order title={"asd"} id={"asd"}/>
            </OrderList>
        </div>
    );
}

export default Test;
