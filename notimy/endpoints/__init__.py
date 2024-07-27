from notimy.endpoints.channels import blueprint as channels_blueprint
from notimy.endpoints.providers import blueprint as providers_blueprint
from notimy.endpoints.spots import blueprint as spots_blueprint
from notimy.endpoints.users import blueprint as users_blueprint

blueprints = [
    channels_blueprint,
    providers_blueprint,
    users_blueprint,
    spots_blueprint,
]

__all__ = [
    "blueprints",
]
