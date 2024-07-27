/**
 * AdminAddBtn - кнопка для создания нового заказа со стороны админа.
 * Отправляет запрос на /add-order и всё.
 */
import React from 'react';
import classNames from 'classnames';
import styles from './AdminAddBtn.module.css'

const AdminAddBtn: React.FC = () => {
    const AddOrder = () => {
        // send add request to backend.
        // update list.
    }
    return (
        <div className={classNames(styles.btnWrap)} >
            <div className={classNames(styles.btn, styles.btnTrapezoidOutline)} onClick={AddOrder}>
                <span>+</span>
            </div>
        </div>)
}
export default AdminAddBtn;
