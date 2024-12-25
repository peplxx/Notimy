import axios from 'axios';
import {handleMockOrders} from "./mockUtils";
import {mock} from "./mockData";


const dev = true;


const getBaseURL = () => {
    const host = window.location.hostname;
    return `https://${host}/api/`;
};

const api = axios.create({
    baseURL: getBaseURL(),
    withCredentials: true
});

// Fetch orders
export const fetchOrders = async () => {
    if (dev) {
        return handleMockOrders();
    }
    try {
        const res = await api.get('/me');
        if (res.data.role !== 'user') {
            throw new Error("You are an admin!");
        }
        return res.data['channels_data'];
    } catch (e) {
        console.error("Error fetching /me", e);
        return [];
    }
};

export const joinChannelSpot = async (id) => {
    try {
        await api.post(`/join/${id}`);
        return true;
    } catch (e) {
        console.error(`Error joining channel spot /join/${id}`, e);
        return false;
    }
};

export const joinChannel = async (id) => {
    try {
        await api.post(`/join/channel/${id}`);
        return true;
    } catch (e) {
        console.log(`Error /join/channel/${id}.`);
        return false;
    }
};
export const deleteOrderApiUser = async (id) => {
    try {
        await api.delete(`/forget/${id}`);
        return true;
    } catch (e) {
        console.log(`Error  /forget/${id}.`);
        return false;
    }
}
export const closeOrderApiAdmin = async (id) => {
    try {
        await api.post(`/spots/close_channel`, {channel_id: id});
        return true;
    } catch (e) {
        console.log(`Error /spots/close_channel/${id}.`);
        return false;
    }
}


export const createChannelAdmin = async () => {
    if (dev) return true;
    try {
        await api.post(`/spots/new_channel`);
        return true;
    } catch (e) {
        console.log(`Error /spots/new_channel`);
        return false;
    }
}

// Fetch orders for admin
export const fetchOrdersAdmin = async () => {
    if (dev) return [mock];
    try {
        const res = await api.get('/me');
        if (res.data.role !== 'spot_user') {
            throw new Error("You are not an admin!");
        }
        return res.data;
    } catch (e) {
        console.error("Error admin /me", e);
        return [];
    }
};

export const adminLogin = async (token) => {
    if (dev) return true;
    try {
        await api.get(`/login?token=${token}`);
        return true;
    } catch (e) {
        console.log(`Error /login?token=${token}`, e);
        return false;
    }
}

export const getMe = async () => {
    if (dev) return {role: 'spot_user', uuid: 'fake_jopa', orders: [mock]}
    try {
        const res = await api.get(`/me`);
        return res.data;
    } catch (e) {
        console.log(`Error /me`, e);
        return false;
    }
}
export const getMeSpot = async () => {
    try {
        const res = await api.get(`/spots/me`);
        return res.data;
    } catch (e) {
        console.log(`Error /spots/me`, e);
        return false;
    }
}


export const sendMessageAdmin = async (id, message) => {
    const data = {
        "message": {
            "text": message
        },
        "channel_id": id
    }
    try {
        await api.post(`/spots/add_message`, data);
        return true;
    } catch (e) {
        console.log(`Error /spots/add_message`, data, e);
        return false;
    }
}

// Функция отправки подписки на сервер
export async function sendSubscriptionToServer(subscription) {
    try {
        const result = await api.post(`/webpush/subscribe`, subscription);
        return result;
    } catch (e) {
        console.log(`Error /webpush/subscribe`, subscription, e);
        return false;
    }
}

