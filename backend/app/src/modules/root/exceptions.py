__all__ = [
    "ProviderDoesntExist",
    "ImpossibleChange"
]

from starlette import status

from app.src.common.exceptions import CustomHTTPException


class ProviderDoesntExist(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[400]["description"],
        )

    responses = {400: {"description": "Provider does not exist!"}}


class ImpossibleChange(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.responses[403]["description"],
        )

    responses = {403: {"description": "Can not change the value!"}}


class SpotDoesntExist(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.responses[404]["description"],
        )

    responses = {404: {"description": "Spot with such id does not exist!"}}
