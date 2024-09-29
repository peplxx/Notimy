import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import 'normalize.css';
import './index.css';
import {sendSubscriptionToServer} from "./utils/api";

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
// Регистрация service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                // Теперь можно регистрировать push-уведомления
            } else {
                console.log('Разрешение на уведомления не предоставлено.');
            }
        });
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                // Проверяем, существует ли подписка
                return registration.pushManager.getSubscription()
                    .then(subscription => {
                        if (!subscription) {
                            // Если подписки нет, подписываем пользователя заново
                            return subscribeUser(registration);
                        } else {
                            // Если подписка существует, отправляем её на сервер для проверки
                            return sendSubscriptionToServer(subscription);
                        }
                    });
            })
            .catch(error => {
                console.log('Ошибка регистрации ServiceWorker или проверки подписки:', error);
            });
    });
}

// Функция подписки пользователя на push-уведомления
function subscribeUser(registration) {
    return registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedVapidKey
    }).then(subscription => {
        console.log(subscription)
        return sendSubscriptionToServer(subscription);
    });
}

