import werkzeug
from fastapi import HTTPException
from fastapi import status

# TODO: HTTP Exceptions
BadTokenException = {
    "code": status.HTTP_403_FORBIDDEN,
    "description": "Token not recognized, access denied!"
}



ProviderAlreadyExists = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="Provider with such name and description already exists!")
