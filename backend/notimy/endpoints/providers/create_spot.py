import json
from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.config.roles import Roles
from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider, Spot, User
from notimy.data.db.models.alias import Alias
from notimy.middleware.token_auth import get_token, provider_auth
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
    spot_user = User(role=Roles.spotUser.value)
    session.add(spot_user)
    session.commit()

    spot = Spot(provider=provider.id, account=spot_user.id)
    provider.spots += 1
    session.add(spot)
    session.commit()
    spot_user.data = json.dumps({
        "token": spot.token
    })
    alias = Alias(base=spot.id)
    session.add(alias)
    session.commit()
    return spot.dict()


__all__ = [
    "blueprint",
]
