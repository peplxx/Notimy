import React, {useContext, useEffect, useState} from 'react';

import styles from './Header.module.css';
import {Link, redirect} from "react-router-dom";
import {AppContext} from "../context/App";

import {Popover, PopoverTrigger, PopoverContent, Button} from "@nextui-org/popover";
import {formatDate} from "../utils/formatDate";
import { MdAccountBox } from "react-icons/md";
import deleteSessionToken from "../utils/deleteSessionToken";

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
    const [accountOpen, setAccountOpen] = useState(false);
    const {me, user_status} = useContext(AppContext);

    const [showImage, setShowImage] = useState(false); // Стейт для показа/скрытия картинки

    const handleImageClick = () => {
        setShowImage(false); // Скрываем изображение при клике
    };

    return (

        <div className={styles.header}>
            <div className={styles.leftHeader}/>
            {withLogo ?
                <div className={styles.centerHeader}>
                    <Link to={'https://t.me/notimy_app'}>
                        <img src='/app/static/logo.svg' alt='logo' className={styles.logo}></img>
                    </Link>
                    <Link to={'https://t.me/notimy_app'} className={styles.text}>
                        <div>
                            <a>OTIMY</a>
                        </div>
                    </Link>
                    {/* <div className={styles.hint} onClick={()=>{setShowImage(false)}}>
                            !
                        </div> */}
                </div>
                :
                <img src='/app/static/logo.svg' alt='logo' className={styles.logo} style={{position: "absolute", left: "1em"}}/>
            }
            {children}
            <div className={styles.rightHeader}>

                <Popover placement='bottom-end'>
                    <PopoverTrigger>
                        <div className={styles.accountBtn}><MdAccountBox className={styles.accountBtnIcon}/></div>
                    </PopoverTrigger>
                    <PopoverContent>
                        <div className={styles.accountInfo}>

                            {user_status === 'spot_user' && <>
                                <p> Касса: <br/> {me.provider_name}</p>
                            </>}
                            <p>id: <br/> {me.id}</p>
                            <p>tg: <br/> {me.tg}</p>
                            <p> role: <br/> {me.role} </p>
                            <p>registered at: <br/> {formatDate(me.registered_at)}</p>
                            <div className={styles.logoutBtn} onClick={deleteSessionToken}>Выйти</div>
                        </div>
                    </PopoverContent>
                </Popover>
            </div>
            {/* {showImage && (
                    <div style={hint_styles.overlay} onClick={handleImageClick}>
                        <img
                            src="/app/static/pwa_hint.png" // Замени на свою картинку
                            alt="pwa_hint"
                            style={hint_styles.image}
                        />
                    </div>
                )} */}
        </div>
    )
};

export default Header
