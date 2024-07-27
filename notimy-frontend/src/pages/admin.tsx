import React from "react";

import Header from '../components/layout/Header/Header';
import AdminAddBtn from "../components/ui/AdminAddBtn/AdminAddBtn";

import styles from '../assets/styles/global.module.css';
import OrderList from "../components/layout/OrderList/OrderList";
import AdminOrder from "@/components/ui/AdminOrder/AdminOrder";


function Admin() {
    return (
        <div className={styles.App}>
            <div className={styles.Background}/>
            <Header/>
            <OrderList>
                <AdminOrder title={"1"} id={"1"}/>
            </OrderList>
        </div>
    )
}

export default Admin;