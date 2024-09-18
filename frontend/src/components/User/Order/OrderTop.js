import React, {useContext, useEffect, useRef, useState} from "react";

import classNames from "classnames";
import styles from './OrderTop.module.css';
import OrderContext from "context/OrderContext";
import {Bulb} from "components/Bulb";
import Slider from "components/Slider";
import {TrashBucketSvg} from "components/svg/TrashBucketSvg";

const OrderTop = () => {
    const {order, backgroundColorStyles} = useContext(OrderContext);
    const {deleteOrder} = useContext(OrderContext);
    const MenuClickable = useRef(null);
    const titleRef = useRef(null); // Reference for the title element

    const [isSideOpen, setIsSideOpen] = useState(false);
    useEffect(() => {
        const resizeTextToFit = () => {
            if (titleRef.current) {
                let fontSize = 2; // Starting size
                titleRef.current.style.fontSize = fontSize + "em";

                while (titleRef.current.scrollWidth > titleRef.current.offsetWidth && fontSize > 0.5) {
                    fontSize -= 0.1;
                    titleRef.current.style.fontSize = fontSize + "em";
                }
            }
        };

        resizeTextToFit(); // Initial resize
        window.addEventListener("resize", resizeTextToFit); // Resize on window resize

        return () => {
            window.removeEventListener("resize", resizeTextToFit); // Clean up the event listener
        };
    }, [order.provider_name]); // Dependency array includes `order.provider_name` in case it changes

    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };
    return (
        <div className={styles.top} style={backgroundColorStyles}>
            <Bulb/>
            <span className={styles.title} ref={titleRef}>{order.provider_name}</span>
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
                {
                    isSideOpen ?
                        <Slider onDone={deleteOrder}
                                sliderColor={'red'}
                                SliderIcon={TrashBucketSvg}
                                parentRef={MenuClickable}
                        />
                        : null
                }
                {/*<DeleteButton MenuClickable={MenuClickable.current}/>*/}
                <span className={styles.code}>{order.code}</span>
                <span className={styles.expandSign}>{"<"}</span>
            </div>
        </div>
    );
};

export default OrderTop;
