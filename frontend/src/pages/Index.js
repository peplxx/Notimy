import React, { useEffect, useState } from 'react';
import OrderList from 'components/User/OrderList';
import { UserProvider } from "context/UserContext";
import Header from "components/Header/Header";
import ScanBtn from "../components/User/ScanBtn";
import { Toaster, toast } from "sonner";
import { sendSubscriptionToServer } from "../utils/api";
import sleep from "../utils/sleep";

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
    const [showImage, setShowImage] = useState(true); // Стейт для показа/скрытия картинки

    useEffect(() => {
        const registerServiceWorkerAndSubscribe = async () => {
            try {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    toast.success('Разрешение на уведомления предоставлено', {duration: 2000});
                } else {
                    toast.error('Разрешение на уведомления не предоставлено', { duration: 2000 });
                }
            } catch (e) {
                toast.error('Ошибка запроса разрешения на уведомления', { duration: 2000 });
            }

            try {
                let register;
                try {
                    register = await navigator.serviceWorker.register('/sw.js', {
                        scope: '/app'
                    });
                } catch (e) {
                    toast.error("Пожалуйста, создайте PWA", { duration: 2000 });
                }

                await sleep(1000);

                let subscription;
                try {
                    subscription = await register.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: convertedVapidKey
                    });
                } catch (e) {
                    toast.error('Ошибка при подписке на уведомления', { duration: 2000 });
                }

                toast.success('Подписка выполнена', { duration: 2000 });

                await sendSubscriptionToServer(subscription);
            } catch (e) {
                toast.error('Ошибка регистрации или подписки', { duration: 2000 });
            }
        };

        registerServiceWorkerAndSubscribe();
    }, []);

    const handleImageClick = () => {
        setShowImage(false); // Скрываем изображение при клике
    };

    return (
        <div>
            <Toaster />
            <Header />
            <UserProvider>
                <OrderList>
                    <ScanBtn />
                </OrderList>
            </UserProvider>

            {/* Условный рендеринг изображения */}
            {showImage && (
                <div style={styles.overlay} onClick={handleImageClick}>
                    <img
                        src="/pwa_hint.png" // Замени на свою картинку
                        alt="pwa_hint"
                        style={styles.image}
                    />
                </div>
            )}
        </div>
    );
};

// Стили для картинки и оверлея
const styles = {
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

export default Home;
