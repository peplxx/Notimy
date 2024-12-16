import React, {useEffect} from 'react';
import OrderList from 'components/User/OrderList';
import {UserProvider} from "context/UserContext";
import Header from "components/Header/Header";
import ScanBtn from "../components/User/ScanBtn";
import {Toaster} from "sonner";
import {registerServiceWorkerAndSubscribe} from "../utils/serviceWorker";


const Home = () => {

    useEffect(() => {
        registerServiceWorkerAndSubscribe();
    }, []);

    return (
        <div>
            <Toaster/>
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
