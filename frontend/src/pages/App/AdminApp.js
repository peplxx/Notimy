import React from 'react';
import OrderList from 'components/OrderList';
import Header from "components/Header";
import AdminAddBtn from "components/Admin/AdminAddBtn";

const AdminApp = ({orders}) => {
    return (
        <div>
            <Header withLogo={false}>
                <h1 style={{
                    position: "absolute",
                    bottom: "-.6em",
                    color: "white",
                    fontSize: "1em"
                }}>
                </h1>
            </Header>
            <OrderList orders={orders} admin={true}>
                <AdminAddBtn/>
            </OrderList>
        </div>
    );
};

export default AdminApp;
