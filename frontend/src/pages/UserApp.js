import React, {useEffect} from 'react';
import OrderList from 'components/User/OrderList';
import {UserProvider} from "context/UserContext";
import Header from "components/Header/Header";
import ScanBtn from "../components/User/ScanBtn";
import {Toaster} from "sonner";
import {registerServiceWorkerAndSubscribe} from "../utils/serviceWorker";


const UserApp = ({orders}) => {

    useEffect(() => {
        registerServiceWorkerAndSubscribe();
    }, []);

    return (
        <div>
            <Toaster/>
            <Header/>
            <OrderList orders={orders}>
                <ScanBtn/>
            </OrderList>
        </div>
    );
};

export default UserApp;
