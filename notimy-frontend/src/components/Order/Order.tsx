import React, { useState, useEffect } from 'react';
import stylesOrder from './Order.module.css';
import stylesOrderHeader from './OrderHeader.module.css';
import stylesOrderFooter from './OrderFooter.module.css';

interface Props {
    title: string;
    description: string;
    color: string;
}

const Order: React.FC<Props> = ({ title, description, color }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [titleFontSize, setTitleFontSize] = useState(1);

    useEffect(() => {
        const calculateFontSize = () => {
            if (title.length <= 8) {
                return 2;
            } else if (title.length <= 10) {
                return 1.5;
            } else if (title.length <= 12) {
                return 1.3;
            } else {
                return 1.1;
            }
        };

        const newFontSize = calculateFontSize();
        setTitleFontSize(newFontSize);
    }, [title]); // обновляем шрифт при изменении title

    const toggleAccordion = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div
            className={`${stylesOrder.order} ${isOpen ? stylesOrder.Opened : stylesOrder.Closed}`}
            onClick={toggleAccordion}
        >
            <div className={`${stylesOrder.header} ${color}`}>
                <span className={stylesOrderHeader.title} style={{ fontSize: `${titleFontSize}em` }}>
                    {title}
                </span>
                <div className={stylesOrderHeader.side}>
                    <div className={stylesOrderHeader.status}></div>
                    <div className={stylesOrderHeader.share}></div>
                </div>
            </div>
            <div className={stylesOrder.footer}>
                {description}
                <div className={stylesOrderFooter.toggleBtn}>...</div>
            </div>
        </div>
    );
};

export default Order;
