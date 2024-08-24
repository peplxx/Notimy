import axios from 'axios';

const getBaseURL = () => {
    // Get the current protocol (http or https)
    const protocol = window.location.protocol;
    // Get the current host (domain)
    const host = window.location.hostname;
    // Set the port you want to use
    const port = 443;

    // Construct the base URL
    return `https://localhost:443/api/`;
};

// Create an Axios instance with the dynamic base URL
const api = axios.create({
    baseURL: getBaseURL(),
    withCredentials: true
});


export const fetchOrders = async () => {
    try {
        const res = await api.get('/me');
        return [...res.data['channels_data'], {
            "id": "b434bb9c-4501-4ad0-a43d-1ebf2df7b046",
            "open": true,
            "code": "4SUMKH",
            "created_at": "2024-08-22T08:02:31.781182",
            "provider_name": "BAZZAR",
            "messages_data": [
                {"text": "test"},
                {"text": "test"},
                {"text": "test"},
                {"text": "test"},
                {"text": "test"},
            ]
        }];
    } catch (e) {
        console.log("Error /me.");
        return [];
    }
    //
    // return [
    //     {
    //         id: 123, title: 'Bazzar', code: "BEBRA", status: true,
    //         messages: ['Hai!', 'Test '.repeat(50), 'Jopa :)', 'a'.repeat(15), 'a'.repeat(15),]
    //     },
    //     {
    //         id: 456, title: 'Pizza', code: "PENIS", status: true,
    //         messages: ['a'.repeat(15), 'b'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15),]
    //     },
    //     {
    //         id: 798, title: 'Pizza', code: "PENIS", status: true,
    //         messages: ['a'.repeat(15), 'b'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15),]
    //     }
    // ]
};

export const joinChannel = async (id) => {
    try {
        const res = await api.post(`/join/${id}`);
        return true;
    } catch (e) {
        console.log(`Error /join/${id}.`);
        return false;
    }
};

export const deleteOrderApiUser = async (id) => {
    try {
        const res = await api.delete(`/forget/${id}`);
        return true;
    } catch (e) {
        console.log(`Error  /forget/${id}.`);
        return false;
    }
}
export const closeOrderApiAdmin = async (id) => {
    try {
        const res = await api.post(`/spots/close_channel`, {channel_id: id});
        return true;
    } catch (e) {
        console.log(`Error /spots/close_channel/${id}.`);
        return false;
    }
}


export const createChannelAdmin = async () => {
    try {
        const res = await api.post(`/spots/new_channel`);
        return true;
    } catch (e) {
        console.log(`Error /spots/new_channel`);
        return false;
    }
}

export const fetchOrdersAdmin = async () => {

    return [
            {
                id: 123, provider_name: "BAZZAR", code: "A1B2C3", status: false,
                messages_data: [{text: "Hi!"}, {text: "Privet!"}, {text: "JOPA()()"}]
            }
        ];
    try {
        const res = await api.get(`/me`);
        // console.log(res.data.channels_data)
        return res.data.channels_data;
    } catch (e) {
        console.log(`Error /spots/me`);
        return [];
    }
}

export const adminLogin = async (token) => {
    try {
        const res = await api.get(`/login?token=${token}`);
        return true;
    } catch (e) {
        console.log(`Error /login?token=${token}`, e);
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
        const res = await api.post(`/spots/add_message`, data);
        return true;
    } catch (e) {
        console.log(`Error /spots/add_message`, data, e);
        return false;
    }
}
