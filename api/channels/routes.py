__all__ = ["blueprint"]

from flask import Blueprint
from flask_pydantic import validate

from data import exceptions
from data.database.manager import get_manager
from data.datatypes import ChanelCreation

from logging import getLogger
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

