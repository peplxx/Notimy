from logging import getLogger

from flask import Blueprint
from flask_login import current_user, login_required, logout_user

log = getLogger("api.users")
blueprint = Blueprint(
    "user_logout",
    __name__
)


@blueprint.route("/logout", methods=["POST", "GET"])
@login_required
def login():
    log.debug("Logging out user [id=%s]", current_user.id)
    logout_user()
    log.debug("Successfully logged out!")
    return {"message": "You successfully logged out."}
