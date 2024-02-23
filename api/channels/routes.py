__all__ = ["blueprint"]

from flask import Blueprint
from flask_pydantic import validate
from starlette import status

from data import exceptions
from data.database import Provider, Channel
from data.database.db_session import get_session
from data.datatypes import ChanelCreation

blueprint = Blueprint(
    "providers",
    __name__,
)


@blueprint.route("/channels", methods=['POST'], status_code=status.HTTP_201_CREATED)
@validate()
def create_channel(data: ChanelCreation):
    session = get_session()
    provider = session.query(Provider).filter(Provider.token == data.token).first()
    if not provider:
        raise exceptions.BadTokenException
    new_channel = Channel(name=data.name, provider=provider.id, messages=[data.start_message, ])
    session.add(new_channel)
    session.commit()
    return {"id": new_channel.id,
            "code": new_channel.code,
            "channel": new_channel.dict}
