import React from "react";

import Header from '../components/layout/Header/Header';
import AdminAddBtn from "../components/ui/AdminAddBtn/AdminAddBtn";

import styles from '../assets/styles/global.module.css';


function Admin() {
    return (
        <div className={styles.App}>
            <div className={styles.Background}/>
            <Header/>
            <AdminAddBtn/>
        </div>
    )
}

export default Admin;