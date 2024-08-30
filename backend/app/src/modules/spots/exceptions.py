__all__ = [
    "WrongAliasName",
    "AliasAlreadyExist",
    "InvalidChannelLink"
]

from starlette import status

from app.src.common.exceptions import CustomHTTPException


class WrongAliasName(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[400]["description"],
        )

    responses = {400: {"description": "Alias name doesnt satisfy length constraint!"}}


class AliasAlreadyExist(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[400]["description"],
        )

    responses = {400: {"description": "Alias with such name already exist!"}}


class InvalidChannelLink(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[400]["description"],
        )

    responses = {400: {"description": "Channel id is invalid!"}}


class ChannelIsNotFound(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[404]["description"],
        )

    responses = {404: {"description": "Channel is not found!"}}
