import styles from './Bulb.module.css';
import classNames from "classnames";


export const Bulb = () => {
    return (
        <>
            <div className={classNames(styles.blink, styles.bulb)} />
        </>
    );
}
