import React, { useEffect, useRef, useState } from "react";
import { TrashBucketSvg } from "@/components/common/TrashBucketSvg";

import styles from './OrderTop/OrderTop.module.css';

interface DeleteButtonProps {
    MenuClickable: HTMLDivElement | null;
    DeleteAction: () => Promise<Boolean>;
}

const DeleteButton: React.FC<DeleteButtonProps> = ({ MenuClickable, DeleteAction }) => {
    const [position, setPosition] = useState(0);
    const [finalPosition, setFinalPosition] = useState(0);
    const [movePercentage, setMovePercentage] = useState(0);
    const [isSwiping, setIsSwiping] = useState(false);

    const startXRef = useRef(0);
    const DeleteBtn = useRef<HTMLDivElement>(null);

    // НАЖАТИЕ
    const handleTouchStart = (e: React.TouchEvent) => {
        startXRef.current = e.touches[0].clientX;
        setIsSwiping(true);
    };
    const handleMouseDown = (e: React.MouseEvent) => {
        startXRef.current = e.clientX;
        setIsSwiping(true);
    };


    // ДВИЖЕНИЕ
    const handleTouchMove = (e: React.TouchEvent) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.touches[0].clientX - startXRef.current;
            if (deltaX >= 0) { // Allow movement only to the right
                setPosition(Math.min(deltaX, MenuClickable.offsetWidth));
            }
        }
    };
    const handleMouseMove = (e: React.MouseEvent) => {
        if (isSwiping && MenuClickable && DeleteBtn.current) {
            const deltaX = e.clientX - startXRef.current;
            if (deltaX >= 0) { // Allow movement only to the right
                setPosition(Math.min(deltaX, MenuClickable.offsetWidth));
            }
        }
    };

    // СТОП ДВИЖЕНИЫ
    const handleEnd = () => {
        setIsSwiping(false);
        if (MenuClickable && DeleteBtn.current) {
            const deleteThreshold = 50; // 50% threshold to trigger delete action

            if (movePercentage >= deleteThreshold) {
                console.log('Delete action triggered');
                setMovePercentage(100);
                setFinalPosition(100); // Move to the end position
                DeleteAction().then((done) => {
                    if (!done) {
                        setFinalPosition(0); // Reset position
                    }
                });
            } else {
                setFinalPosition(0); // Reset position
            }
        }
    };

    useEffect(() => {
        if (MenuClickable && DeleteBtn.current) {
            const elementWidth = MenuClickable.offsetWidth;
            setMovePercentage(Math.min(14 + (position / elementWidth) * 100, 100));
        }
    }, [position, MenuClickable]);

    useEffect(() => {
        if (!isSwiping) {
            setMovePercentage(finalPosition); // Smoothly transition to final position
        }
    }, [finalPosition, isSwiping]);

    return (
        <>
            <div
                className={styles.deleteBtn}
                style={{
                    width: `calc(${movePercentage}%)`,
                    // transform: `translateX(${position}px)`,
                    transition: !isSwiping ? 'width 0.3s ease' : 'none'
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
        </>
    );
};

export default DeleteButton;
