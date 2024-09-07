import React, { useContext, useEffect, useRef, useState } from "react";
import { TrashBucketSvg } from "components/TrashBucketSvg";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";

const DeleteButton = ({ MenuClickable }) => {
    const { deleteOrder } = useContext(AdminOrderContext);

    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);
    const [isMobile, setIsMobile] = useState(false); // New state to check for mobile

    const startXRef = useRef(0);
    const DeleteBtn = useRef(null);

    // Определение, является ли устройство мобильным
    useEffect(() => {
        const checkIfMobile = () => {
            setIsMobile(window.innerWidth <= 800 || 'ontouchstart' in window);
        };

        window.addEventListener('resize', checkIfMobile);
        checkIfMobile(); // Initial check

        return () => {
            window.removeEventListener('resize', checkIfMobile);
        };
    }, []);

    // Обработка свайпов (мобильные устройства)
    const handleTouchStart = (e) => {
        if (isMobile) {
            e.preventDefault(); // Предотвращение конфликтов с кликами
            startXRef.current = e.touches[0].clientX;
            setIsSwiping(true);
        }
    };

    const handleTouchMove = (e) => {
        if (isSwiping && isMobile && MenuClickable && DeleteBtn.current) {
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

    // Обработка нажатий (мышь)
    const handleMouseDown = async (e) => {
        if (!isMobile) {
            e.stopPropagation();
            e.preventDefault(); // Предотвращение конфликтов с касаниями
            await handleEnd(true); // Delete on click for PC
        }
    };

    const handleEnd = async (done = false) => {
        if (MenuClickable && DeleteBtn.current) {
            const deleteThreshold = 75;
            if (deltaPercentage >= deleteThreshold || done) {
                setIsSwiping(false);
                setDeltaPercentage(100);
                if (await deleteOrder()) {
                    setDeltaPercentage(100);
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
            className={styles.deleteBtn}
            style={{
                width: `${deltaPercentage}%`,
                transition: isSwiping ? 'none' : `width 0.5s`
            }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            onMouseDown={handleMouseDown}
            onClick={(e) => e.stopPropagation()}
            ref={DeleteBtn}
        >
            <TrashBucketSvg />
        </div>
    );
};

export default DeleteButton;
