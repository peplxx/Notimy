import sleep from "./sleep";
import { sendSubscriptionToServer } from "./api";

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
    console.log("Registering Service Worker...");
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
            register = await navigator.serviceWorker.register('/app/static/sw.js', {
                scope: '/app'
            });
        } catch (e) {
            console.error('Error registering service worker:', e);
            // toast.error("Пожалуйста, добавьте приложение на главный экран", { duration: 2000 });
        }

        await sleep(1000);

        let subscription;
        try {
            subscription = await register.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedVapidKey
            });
            console.log('Subscription:', subscription);
        } catch (e) {
            console.error('Error subscribing to push manager:', e);
            // toast.error('Пожалуйста, добавьте приложение на главный экран', { duration: 2000 });
        }

        // Send subscription to the server
        if (subscription) {
            await sendSubscriptionToServer(subscription);
        }

    } catch (e) {
        console.error('General error during service worker registration or subscription:', e);
        // toast.error('Пожалуйста, добавьте приложение на главный экран', { duration: 2000 });
    }
};

