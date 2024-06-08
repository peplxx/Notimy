__all__ = ["blueprint"]


from flask import Blueprint
from flask_pydantic import validate

from data import exceptions
from data.database.manager import get_manager
from data.datatypes import ChanelCreation

from logging import getLogger

from data.datatypes.channels import AddMessage

blueprint = Blueprint(
    "channels",
    __name__,
)
log = getLogger("app.channels")

@blueprint.route("/channels", methods=['POST'])
@validate()
def create_channel(body: ChanelCreation):
    # Creation channel from spot
    log.debug(f"Creating channel from spot [token={body.token}]")
    db = get_manager()
    try:
        channel = db.create_channel(data=body)
        return {"id": channel.id,
                "code": channel.code,
                "channel": channel.dict}
    except ValueError:
        raise exceptions.BadTokenException

@blueprint.route("/add_message", methods=['POST'])
@validate()
def add_message_to_channel(body: AddMessage):
    # Creation channel from spot
    log.debug(f"Adding message for spot [token={body.token}]"
              f" channel [id={body.channel}]")
    db = get_manager()
    try:
        db.add_message(spot_token=body.token,channel_id=body.channel,message=body.message)

        return {"message": "Message was successfully added!",
                "details": f"Message: {body.message.message}"}
    except ValueError:
        raise exceptions.BadTokenException
    except AttributeError:
        raise exceptions.ChannelDoesntExist
