__all__ = ["blueprint"]

from flask import Blueprint
from flask_pydantic import validate
from starlette import status

from data import exceptions
from data.database.db_session import get_session
from data.database.manager import get_manager
from data.datatypes import ChanelCreation

blueprint = Blueprint(
    "channels",
    __name__,
)


@blueprint.route("/channels", methods=['POST'])
@validate()
def create_channel(body: ChanelCreation):
    db = get_manager()
    try:
        channel = db.create_channel(data=body)
        return {"id": channel.id,
                "code": channel.code,
                "channel": channel.dict}
    except ValueError:
        raise exceptions.BadTokenException

