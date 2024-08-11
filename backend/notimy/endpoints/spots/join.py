from logging import getLogger
from uuid import UUID

from flask import Blueprint, redirect
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.config import config
from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, Spot, User
from notimy.utils import exceptions

log = getLogger("api.spots")

blueprint = Blueprint(
    'join_channel_via_spot',
    __name__
)


@blueprint.route("/spot/<string:spot_id>", methods=["GET", "POST"])
@login_required
def join_channel(
        spot_id: str,
        user: User = current_user,
        session: Session = get_session(),
):
    spot_id = UUID(spot_id)
    spot: Spot = session.scalar(
        select(Spot).where(Spot.id == spot_id)
    )
    if not spot: raise exceptions.InvalidLink()
    channel_id = spot.last_channel
    if not channel_id: raise exceptions.SpotHasNoChannels()
    channel: Channel = session.scalar(
        select(Channel).where(Channel.id == channel_id)
    )
    channel.add_listener(user.id)
    user_db: User = session.scalar(
        select(User).where(User.id == user.id)
    )
    user_db.add_channel(channel_id)
    session.commit()
    return redirect(config.API_PREFIX+'/me')
