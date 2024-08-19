// frontend_old/src/components/ui/Order/Order.tsx
import React, { useRef, useState } from 'react';
import OrderFooter from './Footer/OrderFooter';
import OrderTop from '@/components/common/OrderTop/OrderTop';
import styles from './Order.module.css';
import classNames from 'classnames';
import CryptoJS from 'crypto-js';
import axiosInstance from "@/utils/axiosInstance";

interface OrderProps {
    id: string;
    provider_name: string;
    code: string;
    closed_at: string;
    onDelete: () => void;
}

const Order: React.FC<OrderProps> = ({ provider_name, id, code, closed_at, onDelete }) => {
    // Референс на блок заказа.
    const orderRef = useRef<HTMLDivElement>(null);

    const [isOpen, setIsOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

    const deleteChannel = async () => {
        // Начинает состояние удаления
        setIsDeleting(true);
        const before = Date.now();
        // const deleted = await axiosInstance.delete('/channel')
        const after = Date.now();
        await new Promise(r => setTimeout(r,  Math.max(0, 900-(after-before))));
        // удалилось и реф существует
        if (orderRef.current) {
            orderRef.current.style.opacity = '0';
            await new Promise(r => setTimeout(r, 300));
            onDelete();
            return true;
        }
        return false;
    };

    const backgroundStyle = backgroundStyleByIdAndStatus(id, true);

    return (
        <div
            ref={orderRef}
            className={
                classNames(
                    styles.order,
                    {
                        [styles.orderClosed]: !isOpen,
                        [styles.orderOpened]: isOpen,
                        [styles.orderSlidingOut]: isDeleting
                    }
                )
            }
            onClick={toggleOrder}
        >
            <OrderTop
                code={code}
                title={provider_name}
                backgroundStyle={backgroundStyle}
                DeleteAction={deleteChannel}
            />
            <OrderFooter
                backgroundStyle={backgroundStyle}
                closed_at={closed_at}
            />
        </div>
    );
};

function backgroundStyleByIdAndStatus(id: string, status: boolean) {

    const hash = CryptoJS.MD5(id).toString(CryptoJS.enc.Hex);
    const hashNumber = parseInt(hash, 16) % 360;

    let mainHue1 = ((hashNumber) % 360);
    if (mainHue1 < 150) mainHue1 += mainHue1 / 150 * 50;
    let mainHue2 = ((mainHue1 + 100) % 360);

    let backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${mainHue2}, 71%, 79%, 1) 10%, hsla(${mainHue1}, 70%, 81%, 1) 60%)`
    };
    if (status) {
        const greenHue2 = (hashNumber % 40) + 100;
        const greenHue1 = ((hashNumber + 30) % 60) + 90;

        backgroundStyle = {
            background: `linear-gradient(345deg, hsla(${greenHue2}, 70%, 85%, 1) 10%, hsla(${greenHue1}, 70%, 70%, 1) 60%)`
        };
    }
    return backgroundStyle
}

export default Order;
