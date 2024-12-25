import React, {useContext, useRef, useState} from "react";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import AdminContext from "context/AdminContext";
import Slider from "components/Slider";
import {TrashBucketSvg} from "components/svg/TrashBucketSvg";
import {AcceptSvg} from "components/svg/AcceptSvg";
import {QRCodeCanvas} from 'qrcode.react';

const OrderTop = ({
                      order,
                      backgroundStyles,
                      isReady,
                      isSideOpen,
                      setIsSideOpen,
                      setIsOpen,
                      isOpen,
                      isQrOpen,
                      setIsQrOpen,
                      deleteOrder, closeOrder, setQrCode
                  }) => {

    const MenuClickable = useRef(null);

    const emSize = parseFloat(getComputedStyle(document.documentElement).fontSize); // Получаем размер 1em в пикселях
    const qrSize = 14 * emSize; // Пример: если 10em


    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };

    return (
        <div className={styles.top} style={backgroundStyles} onClick={() => {
            setIsOpen(!isOpen)
        }}>
            <span className={styles.title}>#{order.code.slice(0, 2)}</span>
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
                {isSideOpen ?
                    isReady ?
                        <Slider parentRef={MenuClickable} SliderIcon={TrashBucketSvg} sliderColor={'red'}
                                onDone={deleteOrder}/>
                        :
                        <Slider parentRef={MenuClickable} SliderIcon={AcceptSvg} sliderColor={'green'}
                                onDone={closeOrder}/>
                    :
                    null
                }

                {/* <span className={styles.code}>{order.code}</span> */}
                {isSideOpen ?
                    <div className={styles.qrCodeBtn} onClick={(e) => {
                        setQrCode(
                            <QRCodeCanvas value={`https://notimy.ru/j/c/${order.id}`} size={qrSize}/>
                        );
                        e.stopPropagation()
                    }}>
                        QR code
                    </div>

                    :
                    <></>
                }

                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
