// components/ui/AdminAddBtn/AdminAddBtn.js
import React from 'react';
import classNames from 'classnames';
import styles from './AdminAddBtn.module.css';

interface AdminAddBtnProps {
    onAddOrder: () => void;
}

const AdminAddBtn: React.FC<AdminAddBtnProps> = ({ onAddOrder }) => {
    return (
        <div className={classNames(styles.btnWrap)}>
            <div className={classNames(styles.btn, styles.btnTrapezoidOutline)} onClick={onAddOrder}>
                <span>+</span>
            </div>
        </div>
    );
};

export default AdminAddBtn;
