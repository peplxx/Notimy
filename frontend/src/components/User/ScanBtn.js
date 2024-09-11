import React, {useState} from 'react';
import styles from './ScanBtn.module.css';
import {ScanSvg} from "components/svg/ScanSvg";
import {Scanner} from '@yudiel/react-qr-scanner';

const ScanBtn = () => {
    const [isOpen, setIsOpen] = useState(false);

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const redirect = (url) => {
        console.log("Redirect to url: ", url)
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
                        <Scanner
                            onScan={(result) => redirect(result[0].rawValue)} onError={(error) => {
                            console.log(error)
                        }}
                            components={{audio: false}}
                        />
                    </div>
                </div>
            )}
        </>
    );
};

export default ScanBtn;
