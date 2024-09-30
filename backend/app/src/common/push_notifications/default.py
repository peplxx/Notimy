from typing import List

from app.config import get_settings
from app.src.common.push_notifications.dto import PushNotification

settings = get_settings()


class DefaultPushNotification(PushNotification):
    icon: str = settings.PUSH_NOTIFICATION_ICON
    vibrate: List[int] = [200, 100, 200, 100, 200]
    url: str = settings.PUSH_NOTIFICATION_URL
