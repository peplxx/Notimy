import React, {useState} from 'react';
import styles from './ScanBtn.module.css';
import {ScanSvg} from "../ScanSvg";
import {Scanner} from '@yudiel/react-qr-scanner';

const ScanBtn = () => {
    const [isOpen, setIsOpen] = useState(false);

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const redirect = (url) => {
        console.log(url)
        window.location.replace(url)
    }

    return (
        <>
            <div className={styles.addBtn} onClick={openModal}>
                <div className={styles.plus}>
                    <ScanSvg/>
                </div>
            </div>

            {isOpen && (
                <div className={styles.modalOverlay}>
                    <div className={styles.modalContent}>
                        <button className={styles.closeBtn} onClick={closeModal}>
                            &times;
                        </button>
                        <Scanner onScan={(result) => redirect(result[0].rawValue)}/>
                    </div>
                </div>
            )}
        </>
    );
};

export default ScanBtn;
