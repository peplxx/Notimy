import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import 'normalize.css';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <img className="backLogo" src='/logo.svg'/>
        <App/>
    </React.StrictMode>
);
