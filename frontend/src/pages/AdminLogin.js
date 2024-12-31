import React, {useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import {adminLogin} from "utils/api";

const AdminLogin = () => {
    const {token} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const loginAdminAndRedirect = async () => {
            try {
                await adminLogin(token);
                navigate('/app');
            } catch (error) {
                console.error("Failed to login admin: ", error);
            }
        };

        loginAdminAndRedirect();
    }, [token, navigate]);

    return <div>Login Admin...</div>;
};

export default AdminLogin;
