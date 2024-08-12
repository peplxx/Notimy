from logging import getLogger

from flask import Blueprint
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.services.spot.logic import get_spot_by_token
from notimy.middleware.token_auth import get_token, spot_auth

blueprint = Blueprint(
    "get_spot",
    __name__,
)
log = getLogger("api.spots")


@blueprint.route("/spots/me", methods=["POST", "GET"])
@spot_auth
def get_spot():
    session: Session = get_session()
    token = get_token()
    return get_spot_by_token(session=session, token=token)


__all__ = [
    "blueprint",
]
