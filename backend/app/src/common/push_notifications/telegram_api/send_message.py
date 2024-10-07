import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from app.config import get_settings
from app.data.db.models import User
from app.src.common.push_notifications.dto import PushNotification
from app.src.middleware.login_manager import manager

settings = get_settings()
bot = telegram.Bot(token=settings.BOT_TOKEN)


def generate_tg_url(user: User):
    session_token = manager.create_access_token(
        data={"id": str(user.id)},
        expires=settings.SESSION_TOKEN_LIFETIME
    )
    return f"notimy.ru/app/{session_token}"


async def send_telegram_message(user: User, push_data: PushNotification):
    if not user.telegram_id:
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Открыть в приложении", url=generate_tg_url(user))]
    ])
    await bot.send_message(chat_id=user.telegram_id, text=push_data.to_telegram_msg, parse_mode=ParseMode.HTML,
                           reply_markup=keyboard)
