from app.config import get_settings
from app.src.common.push_notifications.dto import PushNotification

settings = get_settings()


class DefaultPushNotification(PushNotification):
    icon = settings.PUSH_NOTIFICATION_ICON
    vibrate = [200, 100, 200, 100, 200]
    url = settings.PUSH_NOTIFICATION_URL
