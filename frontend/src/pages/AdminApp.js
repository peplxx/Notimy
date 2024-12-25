import React, {useContext} from 'react';
import OrderList from 'components/Admin/OrderList';
import Header from "components/Header/Header";
import AdminContext, {AdminProvider} from "context/AdminContext";
import AdminAddBtn from "components/Admin/AdminAddBtn";

const AdminApp = ({orders}) => {
    console.log(orders);
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
            <OrderList orders={orders}>
                <AdminAddBtn/>
            </OrderList>
        </div>
    );
};

export default AdminApp;
