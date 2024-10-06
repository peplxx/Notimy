import React, {useContext, useRef, useState} from "react";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import Slider from "components/Slider";
import {TrashBucketSvg} from "components/svg/TrashBucketSvg";
import {AcceptSvg} from "components/svg/AcceptSvg";
import { QRCodeCanvas } from 'qrcode.react';

const OrderTop = () => {
    const {
        order,
        backgroundStyles,
        isReady,
        isSideOpen,
        setIsSideOpen,
        setIsOpen,
        isOpen
    } = useContext(AdminOrderContext);
    const [isQrOpen, setIsQrOpen] = useState(false);

    const {deleteOrder} = useContext(AdminOrderContext);
    const {closeOrder} = useContext(AdminOrderContext);

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
            <span className={styles.title}>#{order.local_number}</span>
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
                    <div className={styles.qrCodeBtn} onClick={(e)=>{ setIsQrOpen(true);e.stopPropagation()}}>
                        QR code
                    </div>
                    :
                    <></>    
                }
                {isQrOpen ? (
                    <>                    <div className={styles.qrCode} onClick={(e) => { setIsQrOpen(false); e.stopPropagation(); }}>
                        <QRCodeCanvas value={`https://notimy.ru/j/c/${order.id}`} size={qrSize} />
                    </div>
                    <div className={styles.darkBackground}></div>
                    </>

                ) : null}

                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
