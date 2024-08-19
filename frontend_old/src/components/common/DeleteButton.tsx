// frontend_old/src/components/common/DeleteButton.tsx
import React, { useEffect, useRef, useState } from "react";
import { TrashBucketSvg } from "@/components/common/TrashBucketSvg";
import styles from './OrderTop.module.css';

interface DeleteButtonProps {
    MenuClickable: HTMLDivElement | null;
    DeleteAction: () => Promise<boolean>;
}

const DeleteButton: React.FC<DeleteButtonProps> = ({ MenuClickable, DeleteAction }) => {
    const [deltaX, setDeltaX] = useState(0);
    const [deltaPercentage, setDeltaPercentage] = useState(0);
    const [finalPosition, setFinalPosition] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);

    const startXRef = useRef(0);
    const DeleteBtn = useRef<HTMLDivElement>(null);

    // Обработка Нажатий
    const handleTouchStart = (e: React.TouchEvent) => {
        startXRef.current = e.touches[0].clientX;
        setIsSwiping(true);
    };
    const handleMouseDown = (e: React.MouseEvent) => {
        startXRef.current = e.clientX;
        setIsSwiping(true);
    };
    const handleTouchMove = (e: React.TouchEvent) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.touches[0].clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };
    const handleMouseMove = (e: React.MouseEvent) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.clientX - startXRef.current;
            setDeltaX(Math.min(deltaX, MenuClickable.offsetWidth));
        }
    };

    const handleEnd = () => {
        if (MenuClickable && DeleteBtn.current) {
            const deleteThreshold = 50;
            if (deltaPercentage >= deleteThreshold) {
                setDeltaPercentage(100);
                DeleteAction().then(done => {
                    if (done) setDeltaPercentage(100);
                });
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
            onMouseDown={handleMouseDown}
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
