
from logging import getLogger
from uuid import UUID

from flask import Blueprint
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, User

log = getLogger("api.spots")

blueprint = Blueprint(
    'user_delete_channel',
    __name__
)


@blueprint.route("/channel/<string:channel_id>", methods=["DELETE"])
@login_required
def forget_channel(
        channel_id: str,
        user: User = current_user,
        session: Session = get_session(),
):
    channel_id = UUID(channel_id)
    channel: Channel = session.scalar(
        select(Channel).where(Channel.id == channel_id)
    )
    if channel_id not in user.channels:
        return {"message": "User doesn't subscribed to this channel!"}
    channel.delete_listener(user.id)
    session.commit()
    user.delete_channel(channel_id)
    session.add(user)
    session.commit()
    return {"message": "You successfully unsubscribed from channel!"}
