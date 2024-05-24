import uuid

from . import Provider, User, Channel, Spot
from .db_session import get_session
from ..datatypes import RegisterProvider, UpdateProviderData, ChanelCreation, RegisterUser, ProviderAuth
from logging import getLogger

manager = None
log = getLogger('manager')


def init_manager() -> None:
    global manager
    global log

    if manager:
        return

    manager = DatabaseManager()
    log = getLogger('manager')


def get_manager():
    global manager
    return manager


class DatabaseManager:
    def __init__(self):
        self.session = get_session()
        log.info('Database manager is initialized!')

    def __get_provider(self, token: str) -> Provider | ValueError:
        log.debug("Getting provider [token=%s]", token)
        provider = self.session.query(Provider).filter(Provider.token == token).first()
        if provider is None:
            log.warning("Provider is not found!")
            raise ValueError("Provider is not found!")
        log.debug("Provider exists!")
        return provider
    def __provider_by_id(self,provider_id: int) -> Provider:
        # TODO: To make an approach for getting a provider from different args in one method
        # for getting by id and token from the same method
        log.debug("Getting provider [id=%s]", str(provider_id))
        provider = self.session.query(Provider).filter(Provider.id == provider_id).first()
        if provider is None:
            log.warning("Provider is not found!")
            raise ValueError("Provider is not found!")
        log.debug("Provider exists!")
        return provider
    def __get_spot(self, token: str) -> Spot | ValueError:
        log.debug("Getting spot [token=%s]", token)
        spot = self.session.query(Spot).filter(
            Spot.token == token).first()
        if spot is None:
            log.warning("Spot is not found!")
            raise ValueError("Spot is not found!")
        log.debug("Spot exists!")
        return spot

    def register_provider(self, data: RegisterProvider) -> Provider:
        log.debug("Registering new provider [token=%s]", data.token)
        provider = self.session.query(Provider).filter(
            Provider.name == data.name).first()
        if provider:
            log.warning("Provider is already registered!")
            return provider
        provider = Provider(name=data.name, description=data.description)
        self.session.add(provider)
        self.session.commit()
        log.debug("Provider registered!")
        return provider

    def update_provider(self, data: UpdateProviderData) -> Provider | ValueError:
        log.debug("Updating provider data [token=%s]", data.token)
        provider = self.__get_provider(data.token)
        provider.name = data.name
        provider.name = data.description
        self.session.commit()
        log.debug("Provider data updated!")
        return provider

    def create_provider_spot(self, token: str) -> Spot | ValueError:
        log.debug("Creating spot for provider [token=%s]", token)
        provider = self.__get_provider(token)
        spot = Spot(info=None, provider=provider.id)
        self.session.add(spot)
        self.session.commit()
        log.debug("Spot created!")
        return spot

    def create_channel(self, data: ChanelCreation) -> Channel | ValueError:
        log.debug("Creating channel from spot [token=%s]", data.token)
        spot = self.__get_spot(data.token)
        channel = Channel(name=data.name,
                          provider=spot.provider,
                          spot=spot.id,
                          messages=[data.start_message])
        self.session.add(channel)
        provider = self.__provider_by_id(spot.provider)
        provider.add_channel(channel)
        spot.add_channel(channel)
        self.session.commit()
        log.debug("Channel successfully added!")
        return channel

    def __get_user(self, id: int):
        user = self.session.query(User).filter(User.id == id).first()
        return user

    def create_user(self) -> User:
        log.debug("Creating new user")
        user = User(listen_to=[])
        self.session.add(user)
        self.session.commit()
        log.debug("Created new user [id=%s]!", user.id)
        return user

    def make_user_listen(self, user_id: int, chanel_id: int) -> None:
        user = self.__get_user(user_id)
        user.add_listen_to(chanel_id)
        self.session.commit()

    def load_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id)
