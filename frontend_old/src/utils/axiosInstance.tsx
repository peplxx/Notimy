// axiosInstance.tsx
import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: "https://localhost:443/api", // Ensure this URL matches your Flask server's address
    withCredentials: true, // Ensures cookies and credentials are sent with requests
});

export default axiosInstance;
