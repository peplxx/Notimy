import React from 'react';
import OrderList from 'components/User/OrderList';
import {UserProvider} from "context/UserContext";
import Header from "components/Header/Header";
const Home = () => {
    return (
        <div>
            <Header/>
            <UserProvider>
                <OrderList />
            </UserProvider>
        </div>
    );
};

export default Home;
