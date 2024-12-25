import React, {useRef} from "react";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import Slider from "components/Slider";
import {TrashBucketSvg} from "components/svg/TrashBucketSvg";
import {AcceptSvg} from "components/svg/AcceptSvg";


const OrderTop = ({
                      order,
                      backgroundStyles,
                      isReady,
                      isSideOpen,
                      setIsSideOpen,
                      setIsOpen,
                      isOpen,
                      deleteOrder,
                      closeOrder,
                      isQrOpen,
                      setIsQrOpen,
                      setQrCode
                  }) => {

    const MenuClickable = useRef(null);

    // ?
    // const emSize = parseFloat(getComputedStyle(document.documentElement).fontSize); // Получаем размер 1em в пикселях
    // const qrSize = 14 * emSize; // Пример: если 10em


    const toggleMenu = (e) => {
        setIsSideOpen(!isSideOpen);
        e.stopPropagation();
    };

    return (
        <div className={styles.top} style={backgroundStyles} onClick={() => {
            setIsOpen(!isOpen)
        }}>
            <span className={styles.title}>#{order.code.slice(0, 2)}</span>
            <div
                className={classNames(styles.side, {
                    [styles.menuClosed]: !isSideOpen,
                    [styles.menuOpened]: isSideOpen,
                })}
                ref={MenuClickable}
                onClick={toggleMenu}
            >
                {/* Close (Finish) order */}
                {isSideOpen && !isReady &&
                    <Slider parentRef={MenuClickable} SliderIcon={AcceptSvg} sliderColor={'green'}
                            onDone={closeOrder}/>
                }
                {/* Remove order */}
                {isSideOpen && isReady &&
                    <Slider parentRef={MenuClickable} SliderIcon={TrashBucketSvg} sliderColor={'red'}
                            onDone={deleteOrder}/>
                }

                {/* <span className={styles.code}>{order.code}</span> */}
                {/* TODO fix qr code*/}
                {/*{isSideOpen &&*/}
                {/*    <div*/}
                {/*        className={styles.qrCodeBtn}*/}
                {/*        onClick={(e) => {*/}
                {/*        setQrCode(*/}
                {/*            <QRCodeCanvas value={`https://notimy.ru/j/c/${order.id}`} size={qrSize}/>*/}
                {/*        );*/}
                {/*        e.stopPropagation()*/}
                {/*    }}>*/}
                {/*        QR code*/}
                {/*    </div>*/}
                {/*}*/}

                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
