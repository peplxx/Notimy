import uuid

from . import Provider, User, Channel
from .db_session import get_session
from ..datatypes import RegisterProvider, UpdateProviderData, ChanelCreation, RegisterUser

manager = None


def init_manager() -> None:
    global manager

    if manager:
        return

    manager = DatabaseManager()


def get_manager():
    global manager
    return manager


class DatabaseManager:
    def __init__(self):
        self.session = get_session()

    def __get_provider(self, token: str) -> Provider:
        provider = self.session.query(Provider).filter(
            Provider.token == token).first()
        if provider is None:
            raise ValueError("Provider is not found!")
        return provider

    def register_provider(self, data: RegisterProvider) -> Provider:
        provider = self.session.query(Provider).filter(
            Provider.name == data.name).first()
        if provider:
            return provider
        provider = Provider(name=data.name, description=data.description)
        self.session.add(provider)
        self.session.commit()
        return provider

    def update_provider(self, data: UpdateProviderData) -> Provider | ValueError:
        provider = self.__get_provider(data.token)
        provider.name = data.name
        provider.name = data.description
        self.session.commit()
        return provider

    def create_channel(self, data: ChanelCreation) -> Channel | ValueError:
        provider = self.__get_provider(data.token)
        print(provider.name)
        channel = Channel(name=data.name,
                          provider=provider.id,
                          messages=[data.start_message])
        print(channel.id)
        self.session.add(channel)
        self.session.commit()
        provider.add_channel(channel)
        self.session.commit()
        return channel

    def __get_user(self, id: int):
        user = self.session.query(User).filter(User.id == id).first()
        return user

    def create_user(self) -> User:
        # user = self.__get_user(user_id)

        user = User(listen_to=[])
        self.session.add(user)
        self.session.commit()
        return user

    def make_user_listen(self, user_id: int, chanel_id: int) -> None:
        user = self.__get_user(user_id)
        user.add_listen_to(chanel_id)
        self.session.commit()

    def load_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id)