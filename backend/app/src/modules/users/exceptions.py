__all__ = [
    "SystemUsersJoinRestrict",
    "SpotDoestHaveChannels",
]

from starlette import status

from app.src.common.exceptions import CustomHTTPException


class SystemUsersJoinRestrict(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.responses[403]["description"],
        )

    responses = {403: {"description": "Alias name doesnt satisfy length constraint!"}}


class SpotDoestHaveChannels(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[404]["description"],
        )

    responses = {404: {"description": "Spot does not have any channel!"}}


class NotSubscribedOrChannelDoesntExist(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[404]["description"],
        )

    responses = {404: {"description": "You are not subscribed to this channel OR channel doesn't exist!"}}
