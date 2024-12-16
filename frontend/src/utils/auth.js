import {useEffect, useState} from "react";
import {getMe} from "./api";

export const useAuth = () => {
    const [isAdmin, setIsAdmin] = useState(null);
    const [loading, setLoading] = useState(true); // Для отслеживания загрузки
    const [isIOS, setIsIOS] = useState(false);
    const [me, setMe] = useState(null);
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const get_me = await getMe(); // Запрос данных пользователя
                setMe(get_me);
                setIsIOS(/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream);
                setIsAdmin(get_me['role'] === 'spot_user'); // Устанавливаем значение isAdmin
            } catch (error) {
                console.error('Ошибка при получении данных пользователя:', error);
                setIsAdmin(false); // В случае ошибки считаем, что не админ
            } finally {
                setLoading(false); // Останавливаем индикатор загрузки
            }
        };
        fetchUser();
    }, []);

    return {isAdmin, loading, isIOS, me};
};
