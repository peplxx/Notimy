import React, { useContext, useEffect, useRef, useState } from "react";
import styles from './CloseChnlBtn.module.css';
import AdminOrderContext from "context/AdminOrderContext";
import classNames from "classnames";
import { AcceptSvg } from "components/AcceptSvg";

const CloseChnlBtn = ({ MenuClickable }) => {
    const { closeOrder, setIsSideOpen, isSideOpen } = useContext(AdminOrderContext);

    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);
    const [isMobile, setIsMobile] = useState(false);

    const startXRef = useRef(0);
    const closeBtn = useRef(null);

    // Проверка на мобильное устройство
    useEffect(() => {
        const checkIfMobile = () => {
            setIsMobile(window.innerWidth <= 768 || 'ontouchstart' in window);
        };

        window.addEventListener('resize', checkIfMobile);
        checkIfMobile(); // Проверка при монтировании компонента

        return () => {
            window.removeEventListener('resize', checkIfMobile);
        };
    }, []);

    // Обработка касаний (мобильные устройства)
    const handleTouchStart = (e) => {
        if (isMobile) {
            e.preventDefault(); // Предотвращение конфликтов с кликами
            startXRef.current = e.touches[0].clientX;
            setIsSwiping(true);
        }
    };

    const handleTouchMove = (e) => {
        if (isSwiping && isMobile && MenuClickable && closeBtn.current) {
            e.preventDefault(); // Предотвращение конфликтов с кликами
            const deltaX = e.touches[0].clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };

    const handleTouchEnd = async (e) => {
        if (isMobile) {
            e.preventDefault(); // Предотвращение конфликтов с кликами
            await handleEnd();
        }
    };

    // Обработка кликов (ПК)
    const handleMouseDown = (e) => {
        if (!isMobile) {
            e.stopPropagation();
            e.preventDefault(); // Предотвращение конфликтов с касаниями
            setIsSwiping(true);
            startXRef.current = e.clientX;
        }
    };

    const handleMouseMove = (e) => {
        if (isSwiping && !isMobile && MenuClickable && closeBtn.current) {
            const deltaX = e.clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };

    const handleMouseUp = async () => {
        if (!isMobile) {
            await handleEnd();
        }
    };

    const handleEnd = async (done = false) => {
        const deleteThreshold = 75;
        setIsSwiping(false);
        if (MenuClickable && closeBtn.current) {
            if (deltaPercentage < deleteThreshold && !done) {
                setDeltaPercentage(0);
                return;
            }
            setDeltaPercentage(100);
            if (await closeOrder()) {
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
                isSideOpen ? styles.menuOpened : styles.menuClosed,
                styles.acceptBackground,
            )}
            style={{
                width: `${deltaPercentage}%`,
                transition: isSwiping ? 'none' : `width 0.5s`
            }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onClick={(e) => e.stopPropagation()}
            ref={closeBtn}
        >
            <AcceptSvg />
        </div>
    );
};

export default CloseChnlBtn;
