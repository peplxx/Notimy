from typing import List

from . import Provider, User, Channel, Spot

from .db_session import get_session
from ..datatypes import RegisterProvider, UpdateProviderData, ChanelCreation, Message
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

    def __provider_by_id(self, provider_id: int) -> Provider:
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
        print(1)
        return spot

    def create_channel(self, data: ChanelCreation) -> Channel | ValueError:
        log.debug("Creating channel from spot [token=%s]", data.token)
        spot = self.__get_spot(data.token)
        channel = Channel(name=data.name,
                          provider=spot.provider,
                          spot=spot.id,
                          messages=[data.start_message])
        self.session.add(channel)
        self.session.commit()
        print(channel.id)
        spot.add_channel(channel)
        log.debug(f"Spot channels: {spot.channels}")
        self.session.commit()
        log.debug("Channel successfully added!")
        return channel

    def __get_user(self, id: int):
        user = self.session.query(User).filter(User.id == id).first()
        return user

    def create_user(self) -> User:
        log.debug("Creating new user")
        user = User()
        self.session.add(user)
        self.session.commit()
        log.debug("Created new user [id=%s]!", user.id)
        return user

    def make_user_listen(self, user_id: int, chanel_id: int) -> None:
        user = self.__get_user(user_id)
        user.add_channel(chanel_id)
        channel = self.get_channel(chanel_id)
        channel.add_listener(user_id)
        self.session.commit()

    def get_spot(self, id: int) -> Spot:
        spot = self.session.query(Spot).filter(Spot.id == id).first()
        if spot is None:
            return None  # TODO: BETTER ERROR HANDLING
        return spot
    def get_channel_by_code(self, code: str) -> Channel:
        channel = self.session.query(Channel).filter(Channel.code == code).first()
        if channel is None:
            return None  # TODO: BETTER ERROR HANDLING
        return channel

    def load_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def assign_channel(self, user: User, channel_id: int):
        user.add_channel(channel_id)
        self.session.commit()

    def get_channel(self, id: int) -> Channel:
        channel = self.session.query(Channel).filter(Channel.id == id).first()
        if channel is None:
            return None  # TODO: BETTER ERROR HANDLING
        return channel

    def users_channels(self, user: User) -> List[dict]:
        print()
        return [self.get_channel(i).dict for i in user.listen_to]

    def add_message(self,spot_token:str,channel_id: int, message:Message):
        spot = self.__get_spot(spot_token)
        channels = spot.channels
        if channel_id not in channels:
            raise AttributeError
        channel = self.get_channel(channel_id)
        channel.add_message(message)
        self.session.commit()
