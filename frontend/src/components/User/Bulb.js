import styles from './Bulb.module.css';
import classNames from "classnames";


const Bulb = ({isReady}) => {

    return (
        <div className={styles.circle}>
            <div className={classNames(
                isReady ? styles.blink : null,
                styles.bulb)
            }
            />
        </div>
    );
}

export default Bulb;
