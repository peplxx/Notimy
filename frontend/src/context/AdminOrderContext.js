import React, {createContext, useState, useContext, useEffect} from 'react';
import getBackground from 'utils/gradientById';
import AdminContext from "./AdminContext";

const AdminOrderContext = createContext();


export const AdminOrderProvider = ({ children, InitOrder }) => {
    const {deleteOrder: deleteOrderContext} = useContext(AdminContext);
    const [order, setOrder] = useState(InitOrder);
    const [isOpen, setIsOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isReady, setIsReady] = useState(false);
    const [backgroundStyles, setBackgroundStyles] = useState(null);

    async function closeOrder() {
        console.log("Channel is closed!");
        setIsReady(true);
        return true;
    }

    async function deleteOrder() {
        setIsDeleting(true);
        const result = await deleteOrderContext(order.id);
        setIsDeleting(result);
        return result;
    }

    useEffect(() => {
        console.log(order.status)
        setIsReady(order.status);
        setBackgroundStyles( getBackground(order.id, false) );
    }, [order]);

    useEffect(() => {
        console.log(isReady)
        if ( isReady ) {
            console.log('change back');
            setBackgroundStyles( {background: `gray`} );
        }
    }, [isReady]);

    return (
        <AdminOrderContext.Provider value={{order, setOrder, isOpen, setIsOpen, isDeleting, deleteOrder, isReady, closeOrder, backgroundStyles}}>
            {children}
        </AdminOrderContext.Provider>
    );
};

export default AdminOrderContext;
