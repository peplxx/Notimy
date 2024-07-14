import React from 'react';
import classNames from 'classnames';
import styles from './AdminAddBtn.module.css'

const AdminAddBtn: React.FC = () => {
    return (
        <div className={classNames(styles.btnWrap)}>
            <a className={classNames(styles.btn, styles.btnTrapezoidOutline)} href="#">
                <span>+</span></a>
        </div>)
}
export default AdminAddBtn;
