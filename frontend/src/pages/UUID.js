import React, {useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';

const UUIDLogin = () => {
    const {token} = useParams(); // Получаем токен из URL
    const navigate = useNavigate();

    useEffect(() => {
        // Сохраняем токен в куки
        if (token) {
            document.cookie = `session_token=${token}; path=/; max-age=${60*60*24*365*10}`; // Устанавливаем срок жизни куки (3600 секунд = 1 час)
            console.log('Token сохранен в куки:', token);
            
            navigate('/app')
        }
    }, [token, navigate]);

    return <div>Login via Telegram...</div>;
};

export default UUIDLogin;
