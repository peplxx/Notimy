__all__ = ["MaxSpotIsReached"]
from starlette import status

from app.src.common.exceptions import CustomHTTPException


class MaxSpotIsReached(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.responses[403]["description"],
        )

    responses = {403: {"description": "Max spot constraint is reached!"}}
