from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.config import config
from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider, Spot
from notimy.middleware.token_auth import provider_auth, get_token
from notimy.schemas.providers import ProviderAuth
from notimy.utils import exceptions

blueprint = Blueprint(
    "create_spot",
    __name__,
)
log = getLogger("api.providers")


@blueprint.route("/providers/new_spot", methods=["POST", ])
@provider_auth
@validate()
def create_provider(
        body: ProviderAuth
):
    session: Session = get_session()
    token = get_token()
    provider = session.scalar(select(Provider).where(Provider.token == token))
    if provider.spots >= provider.max_spots:
        raise exceptions.MaxSpotsLimit
    spot = Spot(provider=provider.id)
    provider.spots += 1
    session.add(spot)
    session.commit()
    return spot.dict()


__all__ = [
    "blueprint",
]
