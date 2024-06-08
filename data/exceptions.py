from fastapi import HTTPException
from fastapi import status

# TODO: HTTP Exceptions
BadTokenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail= "Token not recognized, access denied!"
)

ProviderAlreadyExists = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="Provider with such name and description already exists!")

ChannelDoesntExist = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Channel id is invalid or current spot doesn't have it!")