import React, {useContext, useRef, useState} from "react";
import DeleteButton from "./DeleteButton";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import {Bulb} from "components/Bulb";

const OrderTop = () => {
    const {order, backgroundColorStyles} = useContext(AdminOrderContext);

    const MenuClickable = useRef(null);

    const [isSideOpen, setIsSideOpen] = useState(false);

    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };

    return (
        <div className={styles.top} style={backgroundColorStyles}>
            <Bulb/>
            <span className={styles.title}>{order.title}</span>
            <div
                className={
                    classNames(
                        styles.side,
                        {
                            [styles.menuClosed]: !isSideOpen,
                            [styles.menuOpened]: isSideOpen,
                        }
                    )
                }
                ref={MenuClickable}
                onClick={(e) => {
                    toggleMenu();
                    e.stopPropagation();
                }}
            >
                <DeleteButton MenuClickable={MenuClickable.current}/>
                <span className={styles.code}>{order.code}</span>
                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
