from flask import Blueprint

from notimy.endpoints.spots.join import blueprint as join_channel
from notimy.endpoints.spots.me import blueprint as me
from notimy.endpoints.spots.change_alias import blueprint as change_alias

blueprint = Blueprint(
    "spots",
    __name__
)


includes = [
    join_channel,
    me,
    change_alias,

]

for bp in includes:
    blueprint.register_blueprint(bp)


__all__ = [
    "blueprint",

]