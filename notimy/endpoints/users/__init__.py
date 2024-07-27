from flask import Blueprint

from notimy.endpoints.users.login import blueprint as user_login
from notimy.endpoints.users.logout import blueprint as user_logout
from notimy.endpoints.users.me import blueprint as user_me

blueprint = Blueprint(
    "users",
    __name__
)

include = [
    user_login,
    user_me,
    user_logout
]

for bp in include:
    blueprint.register_blueprint(bp)

__all__ = [
    "blueprint"
]
