import React, {createContext, useState, useContext} from 'react';
import getBackground from 'utils/gradientById';
import AdminContext from "./AdminContext";

const AdminOrderContext = createContext();


export const AdminOrderProvider = ({ children, InitOrder }) => {
    const {deleteOrder: deleteOrderContext} = useContext(AdminContext);
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
        <AdminOrderContext.Provider value={{order, setOrder, isOpen, setIsOpen, isDeleting, deleteOrder, backgroundColorStyles}}>
            {children}
        </AdminOrderContext.Provider>
    );
};

export default AdminOrderContext;
