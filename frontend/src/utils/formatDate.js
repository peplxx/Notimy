export const formatDate = (dateStr) => {
    const date = new Date(dateStr);

    const options = {
        hour: '2-digit',
        minute: '2-digit'
    };

    return date.toLocaleTimeString('ru-RU', options)   + ' | ' +  date.toLocaleDateString('ru-RU');

};