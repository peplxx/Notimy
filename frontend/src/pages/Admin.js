import React from 'react';
import OrderList from 'components/Admin/OrderList';
import Header from "components/Header/Header";
import {AdminProvider} from "context/AdminContext";

const Home = () => {
    return (
        <div>
            <Header>
                <h1 style={{position: "absolute", right: "30%", top: "0.7em", color: "white", fontSize: "0.5em"}}>admin</h1>
            </Header>
            <AdminProvider>
            <OrderList/>
            </AdminProvider>
        </div>
    );
};

export default Home;
