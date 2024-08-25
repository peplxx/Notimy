import React from 'react';
import styles from './ScanBtn.module.css';
import {ScanSvg} from "../ScanSvg";


const ScanBtn = () => {
    return (
        <div className={styles.addBtn}>
            <div className={styles.plus}>
                <ScanSvg/>
            </div>

        </div>
    );
};

export default ScanBtn;
