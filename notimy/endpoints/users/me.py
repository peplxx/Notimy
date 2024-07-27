from logging import getLogger

from flask import Blueprint
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Channel, User

log = getLogger("api.users")
blueprint = Blueprint(
    "user_me",
    __name__
)


@blueprint.route("/me", methods=["POST", "GET"])
@login_required
def login(
        session: Session = get_session()
):
    user: User = current_user
    response = user.dict()
    response["channels"] = []
    for channel_id in user.channels:
        channel = session.scalar(select(Channel).where(Channel.id == channel_id))
        session.rollback()
        if channel.expired:
            # TODO: Proper channel deletion
            # session.delete(channel)
            # session.commit()
            continue
        response["channels"] += [channel.dict()]
    return response
