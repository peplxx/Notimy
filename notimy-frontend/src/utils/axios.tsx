import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: "http://0.0.0.0:5000"
});

export default axiosInstance;
