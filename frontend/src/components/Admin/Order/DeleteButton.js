import React, {useContext, useEffect, useRef, useState} from "react";
import { TrashBucketSvg } from "components/TrashBucketSvg";
import styles from './OrderTop.module.css';
import AdminOrderContext from "context/AdminOrderContext";

const DeleteButton = ({ MenuClickable }) => {
    const {deleteOrder} = useContext(AdminOrderContext);

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

    const handleEnd = async (done = false) => {
        if (MenuClickable && DeleteBtn.current) {
            const deleteThreshold = 75;
            if (deltaPercentage >= deleteThreshold || done) {
                setIsSwiping(false);
                setDeltaPercentage(100);
                if ( await deleteOrder() ) {
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
            onTouchEnd={handleEnd}
            onMouseDown={async (e)=>{
                await handleEnd(true);
                e.stopPropagation();
            }}
            onMouseMove={handleMouseMove}
            onMouseUp={handleEnd}
            onClick={(e) => e.stopPropagation()}
            ref={DeleteBtn}
        >
            <TrashBucketSvg />
        </div>
    );
};

export default DeleteButton;
