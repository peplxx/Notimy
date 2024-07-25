from logging import getLogger

from fastapi import Depends
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, Spot
from notimy.middleware import spot_auth
from flask import Blueprint

from notimy.middleware.token_auth import get_token
from notimy.schemas.channels import AddMessage

log = getLogger("api.channels")

blueprint = Blueprint(
    "add_message",
    __name__,
)


@blueprint.route('/channels/add_message', methods=['POST'])
@spot_auth
@validate()
def add_message_to_channel(
        body: AddMessage
):
    session: Session = get_session()
    token: str = get_token()
    log.debug(f"Adding message to channel on spot [token={token}] [channel_id={body.channel_id}]")
    channel: Channel = session.scalar(select(Channel).where(Channel.id == body.channel_id))
    channel.add_message(body.message)
    session.commit()
    return channel.dict()
