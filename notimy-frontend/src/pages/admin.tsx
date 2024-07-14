import React from "react";

import Header from '../components/layout/Header/Header';
import AdminAddBtn from "../components/ui/AdminAddBtn/AdminAddBtn";

import styles from '../assets/styles/global.module.css';
import OrderList from "../components/layout/OrderList/OrderList";
import Order from "../components/ui/Order/Order";


function Admin() {
    return (
        <div className={styles.App}>
            <div className={styles.Background}/>
            <Header/>
            <AdminAddBtn/>
            {/*<OrderList/>*/}
        </div>
    )
}

export default Admin;