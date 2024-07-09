import axios from 'axios';

const axiosBase = axios.create({
    baseURL: "http://0.0.0.0:5000"
});

export default axiosBase;
