from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, Spot
from notimy.middleware.token_auth import get_token, spot_auth

blueprint = Blueprint(
    "get_spot",
    __name__,
)
log = getLogger("api.spots")



@blueprint.route("/spots/me",methods=["POST","GET"])
@spot_auth
@validate()
def get_spot(
):
    session: Session = get_session()
    token = get_token()
    spot: Spot = session.scalar(select(Spot).where(Spot.token == token))
    response = spot.dict()
    response["channels"] = []
    print(spot.channels)
    for channel_id in spot.channels:
        channel = session.scalar(select(Channel).where(Channel.id == channel_id))
        if channel.expired:
            # TODO: Proper channel deletion
            # session.delete(channel)
            # session.commit()
            continue
        response["channels"] += [channel.dict()]

    return response


__all__ = [
    "blueprint",
]