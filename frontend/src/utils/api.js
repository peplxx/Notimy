import axios from 'axios';

const getBaseURL = () => {
    const host = window.location.hostname;
    return `https://${host}/api/`;
};

// Create an Axios instance with the dynamic base URL
const api = axios.create({
    baseURL: getBaseURL(),
    withCredentials: true
});

const dev = false;


var x = 1;
var mock_list = []
var mock =
    {
        id: "f5e41562-90a2-4fa7-a912-7805072a8286",
        provider: "a2c0d306-550d-4064-bcf9-51c47ea099c3",
        open: true,
        code: "X46WX0",
        created_at: "2024-09-02T13:43:55.494145",
        dispose_at: "2024-09-09T13:43:55.494154",
        closed_at: null,
        local_number: 6,
        spot_id: "c2ab0254-0bb9-4a72-8687-b1710b121e70",
        provider_name: "Sauer Group",
        users_ids: [
            "cce2d0a4-c7a7-435d-9f17-9801e5abe29c"
        ],
        messages_data: [{text: "Bebra1"}, {text: "Bebra2"}, {text: "Bebra3"}, {text: "Bebra4"}, {text: "Bebra5"}]
    }

export const fetchOrders = async () => {
    if (dev) {
        if (x % 2 === 0 && x % 4 !== 0) {
            let new_mock = {...mock};
            new_mock['id'] = x.toString();
            mock_list.push(new_mock);
        } else if (x % 4 === 0) {
            mock_list[mock_list.length - 1]['open'] = false;
        }
        x += 1;
        return [...mock_list];
    }
    try {
        const res = await api.get('/me');
        if (res.data.role !== 'user') {
            throw new Error("You are an admin!");
        }
        return res.data['channels_data'];
    } catch (e) {
        console.log("Error /me.");
        return [];
    }
};

export const joinChannel = async (id) => {
    try {
        await api.post(`/join/${id}`);
        return true;
    } catch (e) {
        console.log(`Error /join/${id}.`);
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
    try {
        await api.post(`/spots/new_channel`);
        return true;
    } catch (e) {
        console.log(`Error /spots/new_channel`);
        return false;
    }
}

export const fetchOrdersAdmin = async () => {
    if (dev) return mock;
    try {
        const res = await api.get(`/me`);
        if (res.data.role !== 'spot_user') {
            throw new Error("You are not an admin!");
        }
        // console.log(res.data.channels_data)
        return res.data;
    } catch (e) {
        console.log(`Error admin /me`, e);
        return [];
    }
}

export const adminLogin = async (token) => {
    try {
        await api.get(`/login?token=${token}`);
        return true;
    } catch (e) {
        console.log(`Error /login?token=${token}`, e);
        return false;
    }
}

export const getMe = async () => {
    if (dev) return {role: 'spot_user'}
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
        await api.post(`/webpush/test`);
        return result;
    } catch (e) {
        console.log(`Error /webpush/subscribe`, subscription, e);
        return false;
    }
}

