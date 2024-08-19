from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from frontend.data.db.models import User
from frontend.endpoints.channels.get_channel import get_channel_by_id
from frontend.data.db.connection import get_session
from frontend.data.db.models import Channel, Spot
from frontend.middleware import spot_auth
from frontend.middleware.token_auth import get_token
from frontend.schemas.channels import CreateChannel

log = getLogger("api.channels")

blueprint = Blueprint(
    "create_channel",
    __name__,
)


@blueprint.route('/channels/new', methods=['POST', "GET"])
@spot_auth
@validate()
def create_channel(
        body: CreateChannel
):
    session: Session = get_session()
    token: str = get_token()
    log.debug(f"Creating channel from spot [token={token}]")
    spot: Spot = session.scalar(select(Spot).where(Spot.token == token))
    channel = Channel(
        name=body.name,
        provider=spot.provider,
        spot=spot.id,
    )
    session.add(channel)
    session.commit()
    spot.add_channel(channel)

    spot_user = session.scalar(select(User).where(User.id == spot.account))
    spot_user.add_channel(channel.id)
    session.add(spot_user)
    session.commit()

    channel.add_listener(spot_user.id)
    session.commit()

    if body.message:
        channel.add_message(body.message)
    session.commit()
    return get_channel_by_id(session,channel.id)
