import React, { useState, useRef, useEffect } from 'react';
import classNames from "classnames";

import stylesTop from './OrderTop.module.css';
import DeleteButton from '@/components/common/DeleteButton';

interface Props {
    title: string;
    backgroundStyle: React.CSSProperties;
    DeleteAction: () => void;
}

const OrderTop: React.FC<Props> = ({ title, backgroundStyle, DeleteAction }) => {
    const MenuClickable = useRef<HTMLDivElement>(null);

    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <div className={stylesTop.top} style={backgroundStyle}>
            <span className={stylesTop.title}>{title}</span>
            <div
                className={classNames(stylesTop.side, {
                    [stylesTop.menuClosed]: !isMenuOpen,
                    [stylesTop.menuOpened]: isMenuOpen,
                })}
                onClick={(e) => {
                    toggleMenu();
                    e.stopPropagation();
                }}
            >
                <DeleteButton MenuClickable={MenuClickable.current} DeleteAction={DeleteAction} />
                <div className={stylesTop.menuClickable} ref={MenuClickable}></div>
                <span className={stylesTop.code}>BEBRA</span>
                <span className={stylesTop.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;