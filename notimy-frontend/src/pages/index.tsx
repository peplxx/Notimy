import React from 'react';
import Header from '../components/layout/Header/Header';
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css';
import Order from '@/components/ui/Order/Order';

function App() {
    return (
        <div className={styles.App}>
            <Header/>
            <OrderList orders={[]}>
                <Order title={"1"} id={"1"}/>
                <Order title={"2"} id={"2"}/>
                <Order title={"3"} id={"3"}/>
                <Order title={"4"} id={"4"}/>
                {/* {null} */}
            </OrderList>
            
        </div>
    );
}

export default App;
