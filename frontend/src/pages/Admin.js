import React from 'react';
import OrderList from 'components/Admin/OrderList';
import Header from "components/Header/Header";
import {AdminProvider} from "context/AdminContext";
import AdminAddBtn from "components/Admin/AdminAddBtn";

const Home = () => {
    return (
        <div>
            <Header>
                <h1 style={{position: "absolute", right: "calc(50% - 9em)", top: "1.16em", color: "white", fontSize: "1em"}}>admin</h1>
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
