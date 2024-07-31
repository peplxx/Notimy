from flask import Blueprint

from notimy.endpoints.channels.add_message import blueprint as add_message
from notimy.endpoints.channels.create import blueprint as create_channel
from notimy.endpoints.channels.forget import blueprint as delete_channel

blueprint = Blueprint(
    "channels",
    __name__,
)
include = [
    create_channel,
    add_message,
    delete_channel
]

for bp in include:
    blueprint.register_blueprint(bp)


__all__ = [
    "blueprint",
]
