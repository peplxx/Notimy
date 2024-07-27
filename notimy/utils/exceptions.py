from werkzeug.exceptions import HTTPException


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
