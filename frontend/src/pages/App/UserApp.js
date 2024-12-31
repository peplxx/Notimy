import React, {useEffect} from 'react';
import OrderList from 'components/OrderList';
import Header from "components/Header";
import ScanBtn from "components/User/ScanBtn";
import {Toaster} from "sonner";
import {registerServiceWorkerAndSubscribe} from "utils/serviceWorker";

const UserApp = ({orders}) => {

    useEffect(() => {
        // Define an async function to call the async logic
        const fetchData = async () => {
            await registerServiceWorkerAndSubscribe(); // Ensure this is only called once
        };

        fetchData(); // Call the async function
    }, []); // Empty dependency array ensures this effect runs only once on mount

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
