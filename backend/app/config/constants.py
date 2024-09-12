from enum import Enum


class Roles(Enum):
    providerUser = "provider_user"
    spotUser = "spot_user"
    default = "user"


NO_DESCRIPTION = "NO_DESCRIPTION"
NO_ADDITIONAL_INFO = "NO_ADDITIONAL_INFO"
