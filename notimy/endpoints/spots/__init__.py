from flask import Blueprint

from notimy.endpoints.spots.join import blueprint as join_channel
from notimy.endpoints.spots.me import blueprint as me

blueprint = Blueprint(
    "spots",
    __name__
)


includes = [
    join_channel,
    me
]

for bp in includes:
    blueprint.register_blueprint(bp)


__all__ = [
    "blueprint",

]