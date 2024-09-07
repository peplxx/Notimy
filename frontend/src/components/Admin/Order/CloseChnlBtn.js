import React, {useContext, useEffect, useRef, useState} from "react";
import styles from './CloseChnlBtn.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import classNames from "classnames";
import { AcceptSvg } from "components/AcceptSvg";

const CloseChnlBtn = ({ MenuClickable }) => {
    const {closeOrder, setIsSideOpen, isSideOpen} = useContext(AdminOrderContext);

    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);

    const startXRef = useRef(0);
    const closeBtn = useRef(null);

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
        if (isSwiping && MenuClickable && closeBtn.current) {
            const deltaX = e.touches[0].clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };
    const handleMouseMove = (e) => {
        if (isSwiping && MenuClickable && closeBtn.current) {
            const deltaX = e.clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };

    const handleEnd = async (done = false) => {
        // Если меньше порога - двигаем в ноль
        // Двигаем в 100
        // Если Операция заебись - закрываем слайдер
        // Двигаем в 0 в конце
        const deleteThreshold = 75;
        setIsSwiping(false);
        if (MenuClickable && closeBtn.current) {
            if (deltaPercentage < deleteThreshold && !done) {
                setDeltaPercentage(0);
                return;
            }
            setDeltaPercentage(100);
            if ( await closeOrder() ) {
                setIsSideOpen(false);
            }
            setDeltaPercentage(0);
        }
    };

    useEffect(() => {
        if (MenuClickable && closeBtn.current) {
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
            onMouseDown={async (e)=>{
                await handleEnd(true);
                e.stopPropagation();
            }}
            // onMouseMove={handleMouseMove}
            // onMouseUp={handleEnd}
            onClick={(e) => e.stopPropagation()}
            ref={closeBtn}
        >
            <AcceptSvg />
        </div>
    );
};

export default CloseChnlBtn;
