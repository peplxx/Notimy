import React, {useContext} from 'react';
import OrderList from 'components/Admin/OrderList';
import Header from "components/Header/Header";
import {AdminProvider} from "context/AdminContext";
import AdminAddBtn from "components/Admin/AdminAddBtn";

const Home = () => {
    return (
        <div>
            <AdminProvider>
                <Header withLogo={false} >
                    <h1 style={{
                        position: "absolute",
                        bottom: "-.6em",
                        color: "white",
                        fontSize: "1em"
                    }}>
                        {/*касса*/}
                    </h1>
                </Header>
                <OrderList>
                    <AdminAddBtn/>
                </OrderList>
            </AdminProvider>
        </div>
    );
};

export default Home;
