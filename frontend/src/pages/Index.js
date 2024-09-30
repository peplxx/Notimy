import React, {useEffect} from 'react';
import OrderList from 'components/User/OrderList';
import {UserProvider} from "context/UserContext";
import Header from "components/Header/Header";
import ScanBtn from "../components/User/ScanBtn";
import {Toaster, toast} from "sonner";
import {sendSubscriptionToServer} from "../utils/api";

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

const Home = () => {
    useEffect(() => {
        const registerServiceWorkerAndSubscribe = async () => {
            try {
                // Регистрация service worker
                const register = await navigator.serviceWorker.register('/sw.js');
                toast(register)
                // Подписываемся на push уведомления
                const subscription = await register.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: convertedVapidKey
                });
                toast(subscription)
                toast.success('Подписка выполнена');

                // Отправляем подписку на сервер
                await sendSubscriptionToServer(subscription);
            } catch (e) {
                toast.error(`Ошибка регистрации или подписки: ${e.message}`);
            }

            // Запрашиваем разрешение на уведомления
            try {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    toast.success('Разрешение на уведомления предоставлено');
                } else {
                    toast.error('Разрешение на уведомления не предоставлено');
                }
            } catch (e) {
                toast.error(`Ошибка запроса разрешения на уведомления: ${e.message}`);
            }
        };

        // Запускаем асинхронную функцию
        registerServiceWorkerAndSubscribe();
    }, []); // Пустой массив зависимостей для выполнения только при монтировании компонента

    return (
        <div>
            <Toaster />
            <Header />
            <UserProvider>
                <OrderList>
                    <ScanBtn />
                </OrderList>
            </UserProvider>
        </div>
    );
};

export default Home;
