import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";
import {getMe} from "./utils/api";

const useAuth = () => {
    const [isAdmin, setIsAdmin] = useState(null);
    const [loading, setLoading] = useState(true); // Для отслеживания загрузки

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const me = await getMe(); // Запрос данных пользователя
                setIsAdmin(me['role'] === 'spot_user'); // Устанавливаем значение isAdmin
            } catch (error) {
                console.error('Ошибка при получении данных пользователя:', error);
                setIsAdmin(false); // В случае ошибки считаем, что не админ
            } finally {
                setLoading(false); // Останавливаем индикатор загрузки
            }
        };
        fetchUser();
    }, []);

    return {isAdmin, loading};
};

const ProtectedRoute = ({ isUser, children }) => {
    const { isAdmin, loading } = useAuth();

    if (loading) {
        // Показать индикатор загрузки, пока данные загружаются
        return <div>Loading...</div>;
    }

    if (!isAdmin && !isUser) {
        // Если пользователь не админ, перенаправляем
        return <Navigate to="/app" />;
    }

    if (isAdmin && isUser) {
        return <Navigate to="/app/admin" />
    }

    // Если пользователь админ, рендерим контент
    return children;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/app" element={
                    <ProtectedRoute isUser={true}>
                        <Index/>
                    </ProtectedRoute>
                }/>
                <Route path="/j/:id" element={<JoinChannel/>}/>
                <Route path="/app/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="/app/admin" element={
                    <ProtectedRoute isUser={false}>
                        <Admin/>
                    </ProtectedRoute>
                }/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
