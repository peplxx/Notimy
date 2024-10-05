__all__ = ["UserNotFound", "JWTIsInvalid", "TelegramUserAlreadyConnected"]

from starlette import status

from app.src.common.exceptions import CustomHTTPException


class UserNotFound(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[self.status_code]["description"],
        )

    responses = {404: {"description": "User not found!"}}


class JWTIsInvalid(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.responses[self.status_code]["description"],
        )

    responses = {403: {"description": "Something is wrong with token!"}}


class TelegramUserAlreadyConnected(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[self.status_code]["description"],
        )

    responses = {400: {"description": "Telegram user is already connected it's account!"}}
