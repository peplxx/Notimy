from flask import Blueprint

from frontend.endpoints.spots.join import blueprint as join_channel
from frontend.endpoints.spots.me import blueprint as me

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