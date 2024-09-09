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


export const fetchOrders = async () => {
    try {
        const res = await api.get('/me');
        if ( res.data.role !== 'user' ) {
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
    try {
        const res = await api.get(`/me`);
        if ( res.data.role !== 'spot_user' ) {
            throw new Error("You are not an admin!");
        }
        // console.log(res.data.channels_data)
        return res.data.channels_data;
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
    return {'role': 'spot_user1'}
    try {
        const res = await api.get(`/me`);
        return res.data;
    } catch (e) {
        console.log(`Error /me`, e);
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
