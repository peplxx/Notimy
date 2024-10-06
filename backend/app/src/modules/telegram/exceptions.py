__all__ = ["UserNotFound", "JWTIsInvalid", "TelegramUserAlreadyConnected"]

from pydantic import BaseModel
from starlette import status

from app.src.common.exceptions import CustomHTTPException


class UserNotFound(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[404]["description"],
        )

    responses = {404: {"description": "User not found!"}}


class JWTIsInvalid(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.responses[403]["description"],
        )

    responses = {403: {"description": "Something is wrong with token!"}}


