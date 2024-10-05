__all__ = ["UserNotFound"]

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
