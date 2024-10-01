import React from 'react';

import styles from './Header.module.css';
import {Link, redirect} from "react-router-dom";


const Header = ({withLogo = true, children}) => {
    return (

        <Link to={'https://t.me/notimy_app'}>
            <div className={styles.header}>
                {withLogo ?
                    <>
                        <img src='/logo.svg' alt='logo' className={styles.logo}></img>
                        <div className={styles.text}>
                            <a>OTIMY</a>

                        </div>
                    </>
                    :
                    <img src='/logo.svg' alt='logo' className={styles.logo}
                         style={{position: "absolute", left: "1em"}}/>
                }
                {children}
            </div>

        </Link>
    )
};

export default Header
