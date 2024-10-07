import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannelSpot from "./pages/JoinChannelSpot";
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";
import UUIDLogin from "./pages/UUID";
import {getMe} from "./utils/api";

const useAuth = () => {
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

const ProtectedRoute = ({ visitingForAdmin, children }) => {
    const { isAdmin, loading, isIOS, me } = useAuth();

    if (loading) {
        // Показать индикатор загрузки, пока данные загружаются
        return <div>Loading...</div>;
    }

    if (!isAdmin && visitingForAdmin) {
        // Если пользователь не админ, перенаправляем
        return <Navigate to="/app" />;
    }

    if (isAdmin && !visitingForAdmin) {
        return <Navigate to="/app/admin" />
    }
    console.log(`isAdmin ${isAdmin}, vForAdmin ${visitingForAdmin}, isIOS ${isIOS}`)
    console.log(`https://t.me/NotimyAppBot?start=uuid=${me['id']}`)
    if (!isAdmin && !visitingForAdmin && isIOS && !me['tg']) {
        console.log('Redirecting to external link for iOS with me=', me);
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        sleep(200);
        window.location.href = `https://t.me/NotimyAppBot?start=uuid=${me['id']}`; // Редирект на внешнюю ссылку
        return null;
    }

    // Если пользователь на странице для своей роли, генерим контент
    return children;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/app" element={
                    <ProtectedRoute visitingForAdmin={false}>
                        <Index/>
                    </ProtectedRoute>
                }/>
                {/* Правильный ли этот роут ? Как внтри елемента, получить токен */}
                <Route path="/app/:token" element={<UUIDLogin />}/> 
                <Route path="/j/:id" element={<JoinChannelSpot/>}/>
                <Route path="/j/c/:id" element={<JoinChannel/>}/>
                <Route path="/app/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="/app/admin" element={
                    <ProtectedRoute visitingForAdmin={true}>
                        <Admin/>
                    </ProtectedRoute>
                }/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
