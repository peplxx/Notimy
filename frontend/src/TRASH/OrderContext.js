// src/context/OrderContext.js
import React, {createContext, useState, useEffect, useContext} from 'react';
import UserContext from "./UserContext";
import getBackground from 'utils/gradientById';

const OrderContext = createContext();


export const OrderProvider = ({ children, InitOrder }) => {
    const {deleteOrder: deleteOrderContext} = useContext(UserContext);
    const [order, setOrder] = useState(InitOrder);
    const [messages, setMessages] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isDeleted, setIsDeleted] = useState(false);
    const [isReady, setIsReady] = useState(false);
    const [backgroundColorStyles, setBackground] = useState(getBackground(order.id, isReady));

    useEffect(() => {
        if ( messages.length !== order.messages_data.length ) {
            setMessages(order.messages_data);
        }
    }, [order, messages]);

    async function deleteOrder() {
        setIsDeleting(true);
        const result = await deleteOrderContext(order.id);
        setIsDeleting(result);
        return result;
    }

    useEffect(() => {
        setOrder(InitOrder);
    }, [InitOrder]);

    useEffect(() => {
        setIsReady(!InitOrder.open);
    }, [InitOrder]);

    useEffect(() => {
        setBackground(getBackground(order.id, isReady));
    }, [isReady])

    return (
        <OrderContext.Provider value={{order, setOrder, isOpen, setIsOpen, isDeleting,
            deleteOrder, isReady, backgroundColorStyles, isDeleted, setIsDeleted, messages}}>
            {children}
        </OrderContext.Provider>
    );
};

export default OrderContext;
