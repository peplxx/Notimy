import React from 'react';
import { Link } from "react-router-dom";

const Landing = () => {
    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            color: "white",
            textAlign: "center",
            margin: "auto",
        }}>
            <p>Скоро здесь появится информация<br /> Рабочее приложение - <Link to={'/app'} style={{ color: 'lightblue' }}>перейти</Link></p>
        </div>
    );
};

export default Landing;
