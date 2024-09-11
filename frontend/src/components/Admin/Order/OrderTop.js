import React, {useContext, useRef} from "react";
import classNames from "classnames";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import Slider from "components/Slider";
import {TrashBucketSvg} from "components/svg/TrashBucketSvg";
import {AcceptSvg} from "components/svg/AcceptSvg";

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
    const {deleteOrder} = useContext(AdminOrderContext);
    const {closeOrder} = useContext(AdminOrderContext);

    const MenuClickable = useRef(null);

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
                    <Slider parentRef={MenuClickable.current} SliderIcon={TrashBucketSvg} sliderColor={'red'}
                            onDone={deleteOrder}/>
                    :
                    <Slider parentRef={MenuClickable.current} SliderIcon={AcceptSvg} sliderColor={'green'}
                            onDone={closeOrder}/>
                    :
                    null
                }

                <span className={styles.code}>{order.code}</span>
                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
