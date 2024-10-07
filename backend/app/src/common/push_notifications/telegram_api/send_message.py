import telegram
from telegram.constants import ParseMode

from app.config import get_settings
from app.src.common.push_notifications.dto import PushNotification

settings = get_settings()
bot = telegram.Bot(token=settings.BOT_TOKEN)


async def send_telegram_message(chat_id: int, push_data: PushNotification):
    await bot.send_message(chat_id=chat_id, text=push_data.to_telegram_msg, parse_mode=ParseMode.HTML)
