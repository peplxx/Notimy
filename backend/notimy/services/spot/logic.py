from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.models import Alias, Channel, Spot


def get_spot_by_token(session: Session, token: str) -> dict:
    spot: Spot = session.scalar(select(Spot).where(Spot.token == token))
    response = spot.dict()
    response["channels"] = []

    for channel_id in spot.channels:
        channel = session.scalar(select(Channel).where(Channel.id == channel_id))
        if channel.expired:
            # TODO: Proper channel deletion
            # session.delete(channel)
            # session.commit()
            continue
        response["channels"] += [channel.dict()]
    alias = session.scalar(select(Alias).where(Alias.base == spot.id))
    response['alias'] = alias.dict()
    return response


def get_spot_by_id(session: Session, spot_id: UUID) -> dict:
    spot: Spot = session.scalar(select(Spot).where(Spot.id == spot_id))
    return get_spot_by_token(session=session, token=spot.token)
