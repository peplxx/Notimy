import {Navigate} from "react-router-dom";
import React from "react";
import {useAuth} from "./auth";

export const ProtectedRoute = ({ visitingForAdmin, children }) => {
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

    // Пока убрал редирект
    // redirectToTg(isAdmin, visitingForAdmin, isIOS, me['tg'], me['id']);

    // Если пользователь на странице для своей роли, генерим контент
    return children;
};

function redirectToTg(isAdmin, visitingForAdmin, isIOS, tg, uid) {
    console.log(`isAdmin ${isAdmin}, vForAdmin ${visitingForAdmin}, isIOS ${isIOS}`)
    console.log(`https://t.me/NotimyAppBot?start=uuid=${uid}`)
    if (!isAdmin && !visitingForAdmin && isIOS && !tg) {
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        sleep(200);
        window.location.href = `https://t.me/NotimyAppBot?start=uuid=${uid}`; // Редирект на внешнюю ссылку
        return null;
    }
}
