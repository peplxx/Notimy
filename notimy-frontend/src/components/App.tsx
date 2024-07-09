import React from 'react';
import Header from './Header';
import Order from "./Order/Order";
import OrderList from "./OrderList/OrderList";
import styles from './App.module.css'
import gradients from './Order/Gradients.module.css'
import 'normalize.css';

function App() {
  return (
    // <Order title="hi" subtitle="asd" />
    <div className={styles.App}>
        <div className={styles.Background}/>
        <Header title="Notimy" />
        <OrderList/>
            {/*<Order title="BAZZAR" description="-Бургер Дмитрий" color={gradients.gradientPinkGreen} />*/}
            {/*<Order title="108 BAR" description="-Медовуха Сергей" color={gradients.gradientYellowPurple} />*/}
            {/*<Order title="InnoMAX" description="-Питса Никита" color={gradients.gradientYellowGreen} />*/}
    </div>
  );
}

export default App;
