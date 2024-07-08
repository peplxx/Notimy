from flask import Blueprint

from notimy.endpoints.channels.add_message import blueprint as add_message
from notimy.endpoints.channels.create import blueprint as create_channel

blueprint = Blueprint(
    "channels",
    __name__,
)
include = [
    create_channel,
    add_message
]

for bp in include:
    blueprint.register_blueprint(bp)


__all__ = [
    "blueprint",
]
