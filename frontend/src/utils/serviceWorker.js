// Публичный VAPID ключ (замените на ваш ключ)
import sleep from "./sleep";
import {sendSubscriptionToServer} from "./api";

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

export const registerServiceWorkerAndSubscribe = async () => {
    try {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
            // toast.success('Разрешение на уведомления предоставлено', {duration: 2000});
        } else {
            // toast.error('Разрешите отправку уведомлений', { duration: 2000 });
        }
    } catch (e) {
        // toast.error('Пожалуйста, добавьте приложение на главный экран', { duration: 2000 });
    }

    try {
        let register;
        try {
            register = await navigator.serviceWorker.register('/sw.js', {
                scope: '/app'
            });
        } catch (e) {
            // toast.error("Пожалуйста, добавьте приложение на главный экран", { duration: 2000 });
        }

        await sleep(1000);

        let subscription;
        try {
            subscription = await register.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedVapidKey
            });
        } catch (e) {
            // toast.error('Пожалуйста, добавьте приложение на главный экран', { duration: 2000 });
        }

        // toast.success('Подписка выполнена', { duration: 2000 });

        await sendSubscriptionToServer(subscription);
    } catch (e) {
        // toast.error('Пожалуйста, добавьте приложение на главный экран', { duration: 2000 });
    }
};