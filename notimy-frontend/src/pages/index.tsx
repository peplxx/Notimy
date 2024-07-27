import React from 'react';
import Header from '../components/layout/Header/Header';
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css';

function App() {
    return (
        <div className={styles.App}>
            <Header/>
            <OrderList orders={[]}>
                {null}
            </OrderList>
            
        </div>
    );
}

export default App;
