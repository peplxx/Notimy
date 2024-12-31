import React, {useEffect, useRef} from 'react';
import {Link, useNavigate} from "react-router-dom";

import styles from './landing.module.css';
import Slider from "../components/Slider";

const Landing = () => {
    const parent = useRef(null);
    const navigate = useNavigate();

    const handleSliderDone = () => {
        navigate('/app'); // Navigate to the '/app' route
    };

    return (
        <>
            {/*<div className={styles.main} ref={parent}>*/}
            {/*    /!*<Slider parentRef={parent} sliderColor={'rgb(130,255,27)'} onDone={handleSliderDone}/>*!/*/}
            {/*    <a className={styles.btn_text}>Открыть приложение</a>*/}
            {/*</div>*/}
            {/*<img className={styles.presentation} src='/app/static/notimy_presentation.jpg' alt="Presentation"/>*/}

            <div className={styles.center}>
                Скоро здесь появится информация. <br/>
                Рабочее приложение - <Link to={'/app'}>перейти</Link>
            </div>
            <div className={styles.icons}>
                <Link to={'https://t.me/notimy_app'}>
                    <svg className={styles.icon} xmlns="http://www.w3.org/2000/svg" viewBox="11000 11000 313333 313333"
                         shape-rendering="geometricPrecision" text-rendering="geometricPrecision"
                         image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd">
                        <path
                            d="M166667 0c92048 0 166667 74619 166667 166667s-74619 166667-166667 166667S0 258715 0 166667 74619 0 166667 0zm80219 91205l-29735 149919s-4158 10396-15594 5404l-68410-53854s76104-68409 79222-71320c3119-2911 2079-3534 2079-3534 207-3535-5614 0-5614 0l-100846 64043-42002-14140s-6446-2288-7069-7277c-624-4992 7277-7694 7277-7694l166970-65498s13722-6030 13722 3951zm-87637 122889l-27141 24745s-2122 1609-4443 601l5197-45965 26387 20619z"/>
                    </svg>
                </Link>
            </div>
        </>
    );
};

export default Landing;
