import React, {useContext, useRef, useState} from "react";
import DeleteButton from "./DeleteButton";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import {Bulb} from "components/Bulb";
import CloseChnlButton from "./CloseChnlButton";

const OrderTop = () => {
        const {order, backgroundStyles, isReady, isSideOpen, setIsSideOpen, setIsOpen, isOpen} = useContext(AdminOrderContext);

    const MenuClickable = useRef(null);

    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };
    console.log(isReady);
    return (
        <div className={styles.top} style={backgroundStyles} onClick={() => {setIsOpen(!isOpen)}}>
            {/*<Bulb/>*/}
            <span className={styles.title}>{order.code}</span>
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

                {isReady ?
                <DeleteButton MenuClickable={MenuClickable.current} isClosed={!isSideOpen} /> :
                <CloseChnlButton MenuClickable={MenuClickable.current} isClosed={!isSideOpen} setIsSideOpen={setIsSideOpen} />}
                <span className={styles.code}>{order.code}</span>
                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
