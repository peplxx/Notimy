import React, {createContext, useEffect, useState} from "react";
import {useAuth} from "../utils/auth";

const AppContext = createContext();

export function AppContextProvider({ children }) {
    // Че я хочу
    // Чтобы здесь были данные
    // О юзере, статус, заказы
    // user = {status: 'admin'/'user'/'anon'}
    // orders = [order1, order2, ...]

    const {me} = useAuth();
    const [status, setStatus] = useState('anon');
    const [orders, setOrders] = useState([]);


    useEffect(() => {
        setStatus(me.role);
        // if ( me.role === 'spot_user' )
    }, [me])

    return (
        <AppContext.Provider value={{
            status,
            orders
        }} >
            {children}
        </AppContext.Provider>
    );
}