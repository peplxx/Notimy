import React from "react";
import MessagesList from "../../MessagesList/MessagesList";

import styles from "../Order.module.css";
import stylesFooter from "./OrderFooter.module.css";

interface Props {
    closed_at: string;
    backgroundStyle: React.CSSProperties;
}

const OrderFooter: React.FC<Props> = ({closed_at, backgroundStyle}) =>
{
    return (
    <div className={styles.footer} style={backgroundStyle}>
        <MessagesList messages={[]}>
            {null}
        </MessagesList>
        <div className={styles.date}>{closed_at}</div>
        <div className={stylesFooter.toggleBtn}>...</div>
    </div>
    )
}

export default OrderFooter;