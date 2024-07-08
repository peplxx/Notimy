from flask import Blueprint

from notimy.endpoints.providers.create import blueprint as create_provider
from notimy.endpoints.providers.create_spot import blueprint as create_spot
from notimy.endpoints.providers.me import blueprint as me_spot
from notimy.endpoints.providers.update import blueprint as update_provider

blueprint = Blueprint(
    "providers",
    __name__,
)

include = [
    create_provider,
    create_spot,
    me_spot,
    update_provider,

]

for bp in include:
    blueprint.register_blueprint(bp)

__all__ = [
    "blueprint",
]
