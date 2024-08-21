import React, {useContext, useEffect, useRef, useState} from "react";
import { TrashBucketSvg } from "components/TrashBucketSvg";
import styles from './CloseChnlBtn.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import classNames from "classnames";
import { AcceptSvg } from "components/AcceptSvg";

const CloseChnlButton = ({ MenuClickable }) => {
    const {closeOrder, setIsSideOpen, isSideOpen} = useContext(AdminOrderContext);

    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);

    const startXRef = useRef(0);
    const DeleteBtn = useRef(null);

    // Обработка Нажатий
    const handleTouchStart = (e) => {
        startXRef.current = e.touches[0].clientX;
        setIsSwiping(true);
    };
    const handleMouseDown = (e) => {
        startXRef.current = e.clientX;
        setIsSwiping(true);
    };
    const handleTouchMove = (e) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.touches[0].clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };
    const handleMouseMove = (e) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };

    const handleEnd = async () => {
        if (MenuClickable && DeleteBtn.current) {
            const deleteThreshold = 65;
            if (deltaPercentage >= deleteThreshold) {
                setIsSwiping(false);
                setDeltaPercentage(100);
                if ( await closeOrder() ) {
                    setIsSideOpen(false);
                } else {
                    setDeltaPercentage(0);
                }
            } else {
                setDeltaPercentage(0);
            }
        }
        setIsSwiping(false);
    };

    useEffect(() => {
        if (MenuClickable && DeleteBtn.current) {
            const elementWidth = MenuClickable.offsetWidth;
            setDeltaPercentage(Math.min(14 + (deltaX / elementWidth) * 100, 100));
        }
    }, [deltaX, MenuClickable]);

    return (
        <div
            className={classNames(
                isSideOpen ? styles.menuOpened: styles.menuClosed,
                styles.acceptBackground,
            )}
            style={{
                width: `${deltaPercentage}%`,
                transition: isSwiping ? 'none' : `width 0.5s`
            }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleEnd}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleEnd}
            onClick={(e) => e.stopPropagation()}
            ref={DeleteBtn}
        >
            <AcceptSvg />
        </div>
    );
};

export default CloseChnlButton;
