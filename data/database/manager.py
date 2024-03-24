from . import Provider, User, Channel
from .db_session import get_session
from ..datatypes import RegisterProvider, UpdateProviderData, ChanelCreation

__factory = None


def init_manager() -> None:
    global __factory

    if __factory:
        return

    __factory = DatabaseManager()


def get_manager():
    global __factory
    return __factory


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
        channel = Channel(name=data.name,
                          provider=provider.id,
                          messages=[data.start_message])
        provider.add_channel(channel)
        self.session.add(channel)
        self.session.commit()
        return channel
