import React from 'react';
import OrderList from 'components/User/OrderList';
import {UserProvider} from "context/UserContext";
import Header from "components/Header/Header";
import ScanBtn from "../components/User/ScanBtn";
const Home = () => {
    return (
        <div>
            <Header/>
            <UserProvider>
                <OrderList>
                    <ScanBtn/>
                </OrderList>
            </UserProvider>
        </div>
    );
};

export default Home;
