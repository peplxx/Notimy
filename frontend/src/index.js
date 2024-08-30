import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import 'normalize.css';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <svg className="backLogo" viewBox="0 0 124 127" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M84.9289 21C70.8214 21 68.0001 29.8521 68.0001 35.8521V45.9553V56.0585C36.5 31 32.5 21 24 21C9.5 21 6.99996 27.8522 7 35.8521V101.706C7 107.206 9.46902 116.558 24.9869 116.558C39.0944 116.558 41.9157 107.706 41.9157 101.706V81.4999C56 96 74.5 116 85 116C100.5 116 102.916 106.5 102.916 100.558V35.8521C102.916 30.3521 100.447 21 84.9289 21Z"
                stroke="#FDFEFF" stroke-width="5"/>
            <g filter="url(#filter0_d_185_69)">
                <path
                    d="M85 116C100 116 102.916 106.5 102.916 100.558V67.5C100.5 72 98 74.5 94.5 74.5C88 74.5 82.5 67.5 68.0001 56.0585C39 31 32.5 21 24 21C9.5 21 6.99996 27.8522 7 35.8521V69C9.5 65 11 62 16.5 62C27 62 70 116 85 116Z"
                    fill="#FDFEFF"/>
                <path
                    d="M85 116C100 116 102.916 106.5 102.916 100.558V67.5C100.5 72 98 74.5 94.5 74.5C88 74.5 82.5 67.5 68.0001 56.0585C39 31 32.5 21 24 21C9.5 21 6.99996 27.8522 7 35.8521V69C9.5 65 11 62 16.5 62C27 62 70 116 85 116Z"
                    stroke="#FDFEFF" stroke-width="5"/>
            </g>
            <path d="M94 12.2559C109.067 12.7328 111.277 23.1066 111.685 29.0927" stroke="#FDFEFF" stroke-width="5"
                  stroke-linecap="round"/>
            <path d="M94 2.70947C116.97 3.48962 120.364 19.6735 121 29.0103" stroke="#FDFEFF" stroke-width="5"
                  stroke-linecap="round"/>
            <defs>
                <filter id="filter0_d_185_69" x="0.5" y="18.5" width="108.916" height="108" filterUnits="userSpaceOnUse"
                        color-interpolation-filters="sRGB">
                    <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                    <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                                   result="hardAlpha"/>
                    <feOffset dy="4"/>
                    <feGaussianBlur stdDeviation="2"/>
                    <feComposite in2="hardAlpha" operator="out"/>
                    <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"/>
                    <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_185_69"/>
                    <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_185_69" result="shape"/>
                </filter>
            </defs>
        </svg>

        <App/>
    </React.StrictMode>
);
