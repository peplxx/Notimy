from logging import getLogger

from flask import Blueprint, session, redirect
from flask_login import current_user, login_user

from notimy.data.db.connection import get_session
from notimy.data.db.models import User

log = getLogger("api.users")
blueprint = Blueprint(
    "user_login",
    __name__
)


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    user = current_user
    db_sess = get_session()
    try:
        log.debug("User [id=%s] already exists!", user.id)
    except AttributeError:
        log.debug("Creating new user")

        user = User()
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)

    previous_url = session.get('previous_url')
    log.debug(f"Redirecting to {previous_url}")
    return redirect(previous_url)
