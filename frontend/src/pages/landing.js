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
            <img className={styles.presentation} src='/notimy_presentation.jpg' alt="Presentation"/>
            <div className={styles.main} ref={parent}>
                <Slider parentRef={parent} sliderColor={'rgb(130,255,27)'} onDone={handleSliderDone} />
                <span className={styles.btn_text}>Открыть приложение</span>
            </div>
        </>
    );
};

export default Landing;
