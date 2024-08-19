from frontend.endpoints.channels import blueprint as channels_blueprint
from frontend.endpoints.providers import blueprint as providers_blueprint
from frontend.endpoints.spots import blueprint as spots_blueprint
from frontend.endpoints.users import blueprint as users_blueprint

blueprints = [
    channels_blueprint,
    providers_blueprint,
    users_blueprint,
    spots_blueprint,
]

__all__ = [
    "blueprints",
]
