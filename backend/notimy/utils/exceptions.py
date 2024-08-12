from werkzeug.exceptions import HTTPException

from notimy.config import config


class BadTokenException(HTTPException):
    code = 403
    description = "Token not recognized, access denied!"


class MaxSpotsLimit(HTTPException):
    code = 403
    description = "Reached max amount of spots!"


class ProviderAlreadyExists(HTTPException):
    code = 200
    description = "Provider with such name and description already exists!"


class ChannelDoesntExist(HTTPException):
    code = 400
    description = "Channel id is invalid or current spot doesn't have it!"


class InvalidLink(HTTPException):
    code = 400
    description = "Something is wrong with invitation link!"


class SpotHasNoChannels(HTTPException):
    code = 400
    description = "This spot has no channels!"


class ProviderDoesntExist(HTTPException):
    code = 400
    description = "Provider doesnt exist!"


class WrongAliasNameSize(HTTPException):
    alias_size: int = config.ALIAS_NAME_SIZE
    code = 400

    def __init__(self):
        super().__init__(
            description=f"Wrong length for alias size (length = {self.alias_size})!"
        )

class AliasIsTaken(HTTPException):
    code = 400
    description = "This alias name is already taken!"
