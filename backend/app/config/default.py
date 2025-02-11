from datetime import timedelta
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).parents[3] / '.env'
load_dotenv(dotenv_path=env_path)


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "default")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api")
    APP_HOST: str = environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 5000))
    APP_HOSTNAME: str = environ.get("APP_HOSTNAME", "notimy.ru")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "postgres")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)
    DB_USE_SSL: bool = environ.get("DB_USE_SSL", False)

    TESTING: bool = environ.get("TESTING", False)

    # to get a string like this run: "openssl rand -hex 32"
    SECRET_KEY: str = environ.get("SECRET_KEY", "")
    ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

    # Length constraints
    PROVIDER_TOKEN_SIZE: int = 50
    SPOT_TOKEN_SIZE: int = 40
    ALIAS_NAME_SIZE: int = 10
    INVITATION_CODE_SIZE: int = 6
    CHANNEL_LIFETIME: timedelta = timedelta(days=1)
    SESSION_TOKEN_LIFETIME: timedelta = timedelta(weeks=3600)

    ROOT_TOKEN: str = environ.get("ROOT_TOKEN", "gUg8iTYWxbGQPFZJc0c7CS5RZQ9MVXawYHJ9WESUMeERNW2YmX")
    BOT_TOKEN: str = environ.get("BOT_TOKEN", False)

    VAPID_PUBLIC_KEY: str = environ.get("VAPID_PUBLIC_KEY", "")
    VAPID_PRIVATE_KEY: str = environ.get("VAPID_PRIVATE_KEY", "")
    GOOGLE_VAPID_CLAIMS: dict = {"sub": "mailto:notimy_oficial@gmail.com", "aud": "https://fcm.googleapis.com"}
    FIREFOX_VAPID_CLAIMS: dict = {"sub": "mailto:notimy_oficial@gmail.com", "aud": "https://updates.push.services"
                                                                                   ".mozilla.com"}
    APPLE_VAPID_CLAIMS: dict = {"sub": "mailto:notimy_oficial@gmail.com", "aud": "https://api.push.apple.com"}
    PUSH_NOTIFICATION_ICON: str = environ.get("PUSH_NOTIFICATION_ICON", "https://notimy.ru/logo_circle.png")
    PUSH_NOTIFICATION_URL: str = environ.get("PUSH_NOTIFICATION_URL", "https://notimy.ru/app")

    def vapid_claims(self, firefox: bool = False, apple: bool = False) -> dict:
        if firefox:
            return self.FIREFOX_VAPID_CLAIMS
        if apple:
            return self.APPLE_VAPID_CLAIMS
        return self.GOOGLE_VAPID_CLAIMS

    @property
    def is_dev(self) -> bool:
        return self.ENV == 'dev'

    @property
    def is_test(self) -> bool:
        return self.TESTING

    @property
    def cookie_domain(self):
        if self.is_test or self.is_dev:
            return None
        return self.APP_HOSTNAME

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def docs_path(self) -> str | None:
        """
        path for docs
        """
        if self.ENV == "default":
            return "/swagger"
        return None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
