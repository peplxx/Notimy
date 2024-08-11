from logging import getLogger
from uuid import UUID

from flask import Blueprint
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, Provider

log = getLogger("api.channels")

blueprint = Blueprint(
    'get_channel_by_id',
    __name__
)


def get_channel_by_id(session: Session, channel_id: UUID):
    channel: Channel = session.scalar(
        select(Channel).where(Channel.id == channel_id)
    )
    data = channel.dict()
    provider: Provider = session.scalar(
        select(Provider).where(Provider.id == channel.provider)
    )
    data["provider_name"] = provider.name
    return data


@blueprint.route("/channel/<string:channel_id>", methods=["GET"])
def forget_channel(
        channel_id: str,
        session: Session = get_session(),
):
    channel_id = UUID(channel_id)
    return get_channel_by_id(session, channel_id)
