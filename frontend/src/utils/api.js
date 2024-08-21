import axios from 'axios';

const getBaseURL = () => {
    // Get the current protocol (http or https)
    const protocol = window.location.protocol;
    // Get the current host (domain)
    const host = window.location.hostname;
    // Set the port you want to use
    const port = 8000;

    // Construct the base URL
    return `${protocol}//${host}:${port}`;
};

// Create an Axios instance with the dynamic base URL
const api = axios.create({
    baseURL: getBaseURL(),
});


export const fetchOrders = async () => {
    try {
        const res = await api.get('/me');
        return res.channels;
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
        console.log(`Error /forget/${id}.`);
        return false;
    }
}
export const deleteOrderApiAdmin = async (id) => {
    try {
        const res = await api.post(`/spots/close_channel/${id}`, {channel_id: id});
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
    try {
        const res = await api.get(`/spots/me`);
        return res.channels;
    } catch (e) {
        console.log(`Error /spots/me`);
        return false;
    }
    // return {
    //     orders: [
    //         {
    //             id: 123, title: "BAZZAR", code: "A1B2C3", status: false,
    //             messages: ["Hi!", "Privet!", "JOPA()()"]
    //         }
    //     ]
    // };
}
