import React from 'react';
import Header from '../components/layout/Header/Header';
import Order from "../components/ui/Order/Order";
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css'
import gradients from '../assets/styles/Gradients.module.css'

function App() {
  return (
    // <Order title="hi" subtitle="asd" />
    <div className={styles.App}>
        <div className={styles.Background}/>
        <Header title="Notimy" />
        <OrderList/>
            <Order title="BAZZAR" description="-Бургер Дмитрий" color={gradients.gradientPinkGreen} />
            <Order title="108 BAR" description="-Медовуха Сергей" color={gradients.gradientYellowPurple} />
            <Order title="InnoMAX" description="-Питса Никита" color={gradients.gradientYellowGreen} />
    </div>
  );
}

export default App;
