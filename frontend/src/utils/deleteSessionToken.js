import {logoutApi} from "./api";

export default async function deleteSessionToken() {
    // Устанавливаем cookie с именем 'session_token' и истекающим сроком действия в прошлом
    console.log('deleteSessionToken');
    await logoutApi();
}