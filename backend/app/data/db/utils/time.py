import datetime
from app.config import get_settings

config = get_settings()


def get_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None)


def get_dispose_at() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None) + config.CHANNEL_LIFETIME
