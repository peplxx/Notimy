import styles from './Bulb.module.css';
import classNames from "classnames";
import {useContext} from "react";
import OrderContext from "context/OrderContext";


export const Bulb = () => {

    const {isReady} = useContext(OrderContext);

    return (
        <>
            <div className={classNames(
                isReady ? styles.blink : null,
                styles.bulb)
            }
            />
        </>
    );
}
