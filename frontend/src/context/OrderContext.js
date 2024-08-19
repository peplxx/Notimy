// src/context/OrderContext.js
import React, {createContext, useState, useEffect, useContext} from 'react';
import UserContext from "./UserContext";
import getBackground from 'utils/gradientById';

const OrderContext = createContext();


export const OrderProvider = ({ children, InitOrder }) => {
    const {deleteOrder: deleteOrderContext} = useContext(UserContext);
    const [order, setOrder] = useState(InitOrder);
    const [isOpen, setIsOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    async function deleteOrder() {
        setIsDeleting(true);
        const result = await deleteOrderContext(order.id);
        setIsDeleting(result);
        return result;
    }

    const backgroundColorStyles = getBackground(order.id, false);

    return (
        <OrderContext.Provider value={{order, setOrder, isOpen, setIsOpen, isDeleting, deleteOrder, backgroundColorStyles}}>
            {children}
        </OrderContext.Provider>
    );
};

export default OrderContext;
