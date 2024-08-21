import React from 'react';
import OrderList from 'components/Admin/OrderList';
import Header from "components/Header/Header";
import {AdminProvider} from "context/AdminContext";
import AdminAddBtn from "components/Admin/Order/AdminAddBtn";

const Home = () => {
    return (
        <div>
            <Header>
                <h1 style={{position: "absolute", right: "24%", top: "1.8em", color: "white", fontSize: "0.5em"}}>admin</h1>
            </Header>
            <AdminProvider>
                <OrderList>
                    <AdminAddBtn/>
                </OrderList>
            </AdminProvider>
        </div>
    );
};

export default Home;
