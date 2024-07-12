import React from 'react';
import Header from '../components/layout/Header/Header';
import Order from "../components/ui/Order/Order";
import OrderList from "../components/layout/OrderList/OrderList";
import styles from '../assets/styles/global.module.css';

function App() {
  return (
    // <Order title="hi" subtitle="asd" />
      <div className={styles.App}>
          {/*<div className={styles.Background}/>*/}
          <Header/>
          <OrderList/>
          <Order title="BAZZAR" description="-Бургер Дмитрий" id="123"/>
          <Order title="108 BAR" description="-Медовуха Сергей" id="456"/>
          <Order title="InnoMAX" description="-Питса Никита" id="789"/>
          <Order title="InnoMAX" description="-Питса Никита" id="asdfasdjfhbvnxcm"/>
          <Order title="InnoMAX" description="-Питса Никита" id="5"/>
          <Order title="InnoMAX" description="-Питса Никита" id="asd"/>
          <Order title="InnoMAX" description="-Питса Никита" id="75as5"/>
          <Order title="InnoMAX" description="-Питса Никита" id="712sd234"/>
          <Order title="InnoMAX" description="-Питса Никита" id="78asd234"/>
      </div>
  );
}

export default App;
