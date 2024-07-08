from flask import Blueprint
from notimy.endpoints.channels.create import blueprint as create_channel

blueprint = Blueprint(
    "channels",
    __name__,
)

blueprint.register_blueprint(create_channel)


__all__ = [
    "blueprint",
]