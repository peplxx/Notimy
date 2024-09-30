import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import 'normalize.css';
import './index.css';
import {sendSubscriptionToServer} from "./utils/api";
import sleep from "./utils/sleep";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <img className="backLogo" src='/logo.svg' alt="backlogo"/>
        <App/>
    </React.StrictMode>
);
// Публичный VAPID ключ (замените на ваш ключ)
const vapidPublicKey = 'BFvjzC0mYeMAWz9rJCl1EuNSsWpK_1ZEk_JjFzb_VSjAx9_cMtexEBm5pCcMz2mo2IqAqQ0JmlBoyckdpkTDO10';
const convertedVapidKey = urlBase64ToUint8Array(vapidPublicKey);

// Функция для конвертации ключа VAPID
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

window.addEventListener('load', async () => {
    const register = await navigator.serviceWorker.register('/worker.js', {
        scope: '/'
    });

    // Подписываемся на push уведомления
    const subscription = await register.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
    });

    // Если подписка существует, отправляем её на сервер для проверки
    sendSubscriptionToServer(subscription);

    await sleep(1000);

    Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
            // Теперь можно регистрировать push-уведомления
        } else {
            console.log('Разрешение на уведомления не предоставлено.');
        }
    });
});
