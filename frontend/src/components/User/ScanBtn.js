import React, { useState } from 'react';
import styles from './ScanBtn.module.css';
import { ScanSvg } from "../ScanSvg";
import { Scanner } from '@yudiel/react-qr-scanner';

const ScanBtn = () => {
    const [isOpen, setIsOpen] = useState(false);

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    return (
        <>
            <button className={styles.addBtn} onClick={openModal}>
                <div className={styles.plus}>
                    <ScanSvg />
                </div>
            </button>

            {isOpen && (
                <div className={styles.modalOverlay}>
                    <div className={styles.modalContent}>
                        <button className={styles.closeBtn} onClick={closeModal}>
                            &times;
                        </button>
                        <Scanner onScan={(result) => console.log(result)} />
                    </div>
                </div>
            )}
        </>
    );
};

export default ScanBtn;
