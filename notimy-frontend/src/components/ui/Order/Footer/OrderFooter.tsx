import React from "react";
import MessagesList from "../../MessagesList/MessagesList";

import styles from "../Order.module.css";
import stylesFooter from "./OrderFooter.module.css";

interface Props {
    backgroundStyle: React.CSSProperties;
}

const OrderFooter: React.FC<Props> = ({backgroundStyle}) =>
{
    return (
    <div className={styles.footer} style={backgroundStyle}>
        <MessagesList messages={[]}>
            {null}
        </MessagesList>
        <div className={styles.date}>02.08.2024 | 11:11</div>
        <div className={stylesFooter.toggleBtn}>...</div>
    </div>
    )
}

export default OrderFooter;