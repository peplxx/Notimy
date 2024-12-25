import React, {useEffect, useState} from 'react';

import styles from './Header.module.css';
import {Link, redirect} from "react-router-dom";


// Стили для картинки и оверлея
const hint_styles = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 2000,
    },
    image: {
        width: '80%',
        maxWidth: '800px',
        height: 'auto',
        cursor: 'pointer',
    },
};


const Header = ({withLogo = true, children}) => {
    const [showImage, setShowImage] = useState(false); // Стейт для показа/скрытия картинки

    const handleImageClick = () => {
        setShowImage(false); // Скрываем изображение при клике
    };

    return (

        <div className={styles.header}>
            {withLogo ?
                <>
                    <Link to={'https://t.me/notimy_app'}>
                        <img src='/logo.svg' alt='logo' className={styles.logo}></img>
                    </Link>
                    <Link to={'https://t.me/notimy_app'}>
                        <div className={styles.text}>
                            <a>OTIMY</a>
                        </div>
                    </Link>
                    {/* <div className={styles.hint} onClick={()=>{setShowImage(false)}}>
                            !
                        </div> */}
                </>
                :
                <img src='/logo.svg' alt='logo' className={styles.logo}
                     style={{position: "absolute", left: "1em"}}/>
            }
            {children}

            {/* {showImage && (
                    <div style={hint_styles.overlay} onClick={handleImageClick}>
                        <img
                            src="/pwa_hint.png" // Замени на свою картинку
                            alt="pwa_hint"
                            style={hint_styles.image}
                        />
                    </div>
                )} */}
        </div>
    )
};

export default Header
