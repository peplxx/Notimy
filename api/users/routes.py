__all__ = ["blueprint"]

from flask import Blueprint
from flask_login import login_required, current_user

from data.database.manager import get_manager

blueprint = Blueprint(
    "users",
    __name__,
)


@blueprint.route("/spot/<int:spot_id>",methods=['POST',"GET"])
@login_required
def join_channel(spot_id: int):
    manager = get_manager()
    spot = manager.get_spot(spot_id)
    if spot is None:
        return {"message": "Spot doesn't exist!"}
    if spot.lastChannel is None:
        return {"message": "Spot doesn't have a channel"}
    manager.make_user_listen(current_user.id, spot.lastChannel)
    return {"message": "You were successfully joined the channel"}

@blueprint.route("/join/<string:code>",methods=['POST',"GET"])
@login_required
def join_channel_by_code(code: int):
    manager = get_manager()
    channel = manager.get_channel_by_code(code)
    if channel is None:
        return {"message": "Invite code is not valid!"}

    manager.make_user_listen(current_user.id, channel.id)
    return {"message": "You were successfully joined the channel"}