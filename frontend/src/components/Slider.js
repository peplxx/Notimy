import React, {useContext, useEffect, useRef, useState} from "react";
import styles from './Slider.module.css';
import classNames from "classnames";
import {AcceptSvg} from "components/svg/AcceptSvg";
import {TapAndMoveSvg} from "components/svg/TapAndMoveSvg";
import {ClickSvg} from "components/svg/ClickSvg";

const Slider =
    ({
        parentRef,
        onNotDone = () => {
        },  // Функция закрытия слайдера
        onDone = () => {
        },
        SliderIcon = AcceptSvg,  // Иконка слайдера
        sliderColor = 'rgba(0,0,0,0.2)',  // Цвет слайдера
    }) => {
    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);
    const [isMobile, setIsMobile] = useState(null);

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

    const handleTouchStart = (e) => {
        if (isMobile) {
            startXRef.current = e.touches[0].clientX;
            setIsSwiping(true);
        }
    };

    const handleTouchMove = (e) => {
        if (isSwiping && isMobile) {
            const deltaX = e.touches[0].clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, parentRef.offsetWidth));
        }
    };

    const handleTouchEnd = async () => {
        if (isMobile) {
            await handleEnd();
        }
    };

    const handleMouseDown = async (e) => {
        if (!isMobile) {
            e.stopPropagation();
            e.preventDefault();
            await handleEnd(true);
        }
    };

    const handleEnd = async (done = false) => {
        const deleteThreshold = 75;
        setIsSwiping(false);
        if (deltaPercentage < deleteThreshold && !done) {
            setDeltaPercentage(0);
            onNotDone(); // Вызов функции, если слайдер не закрыт
            return;
        }
        setDeltaPercentage(100);
        await onDone();
        setDeltaPercentage(0);
    };

    useEffect(() => {
        const elementWidth = parentRef?.offsetWidth;
        setDeltaPercentage(Math.min(14 + (deltaX / elementWidth) * 100, 100));
    }, [deltaX, parentRef]);

    return (
        <div
            className={classNames(
                // isSideOpen ? styles.menuOpened : styles.menuClosed,
                styles.background
            )}
            style={{
                width: `${deltaPercentage}%`,
                transition: isSwiping ? 'none' : 'width 0.5s',
                backgroundColor: sliderColor,
            }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            onMouseDown={handleMouseDown}
            onClick={(e) => e.stopPropagation()}
            ref={closeBtn}
        >
            <SliderIcon/>
            <div className={styles.hint}>
                {isMobile ? <TapAndMoveSvg/> : <ClickSvg/>}
            </div>
        </div>
    );
};

export default Slider;
