import React, { useRef, useState } from 'react';
import OrderFooter from './Footer/OrderFooter';
import OrderTop from '@/components/common/OrderTop/OrderTop';
import styles from './Order.module.css';
import classNames from 'classnames';
import CryptoJS from 'crypto-js';
import axiosInstance from '@/utils/axios';

interface OrderProps {
    title: string;
    id: string;
}

const Order: React.FC<OrderProps> = ({ title, id }) => {
    const orderRef = useRef<HTMLDivElement>(null); // Убедитесь, что типизация правильная
    const [isOpen, setIsOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    const toggleOrder = () => {
        setIsOpen(!isOpen);
    };

    const hash: string = CryptoJS.MD5(id).toString(CryptoJS.enc.Hex);
    const hashNumber: number = parseInt(hash, 16) % 360;

    let mainHue1 = ((hashNumber) % 360);
    if (mainHue1 < 150) mainHue1 += mainHue1 / 150 * 50;
    let mainHue2 = ((mainHue1 + 100) % 360);
    let backgroundStyle = {
        background: `linear-gradient(345deg, hsla(${mainHue2}, 71%, 79%, 1) 10%, hsla(${mainHue1}, 70%, 81%, 1) 60%)`
    };

    if (title === 'BAZZAR') { // Используйте строгое равенство для сравнения строк
        const greenHue2 = (hashNumber % 40) + 100; // Диапазон 90-150
        const greenHue1 = ((hashNumber + 30) % 60) + 90;

        backgroundStyle = {
            background: `linear-gradient(345deg, hsla(${greenHue2}, 70%, 85%, 1) 10%, hsla(${greenHue1}, 70%, 70%, 1) 60%)`
        };
    }

    async function deleteChannel() {
        // Успешный сценарий, без запроса на бэк.
        setIsDeleting(true);
        await new Promise(r => setTimeout(r, 900));
        orderRef?.current?.remove();
        return true;

        // return axiosInstance.delete(`api/channel/${id}`).then(async (response) => {
        //     if (response.status === 200) {
        //         setIsDeleting(true);
        //         await new Promise(r => setTimeout(r, 500));
        //         orderRef.current.remove();
        //         return true;
        //     }
        //     return false;
        // }).catch(async (e) => {
        //     return false;
        // });
    };

    return (
        <div
            ref={orderRef}
            className={classNames(styles.order, {
                [styles.orderClosed]: !isOpen,
                [styles.orderOpened]: isOpen,
            },
                {
                    [styles.orderSlidingOut]: isDeleting
                }
            )}
            onClick={toggleOrder}
        >
            <OrderTop title={title} backgroundStyle={backgroundStyle} DeleteAction={deleteChannel} />
            <OrderFooter backgroundStyle={backgroundStyle} />
        </div>
    );
};

export default Order;
