from logging import getLogger

from flask import Blueprint, redirect
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.config import config
from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider
from notimy.middleware.token_auth import root_auth, get_token
from notimy.schemas.providers import MaxSpotLimit
from notimy.utils import exceptions

blueprint = Blueprint(
    "change_maxspot_limit",
    __name__,
)
log = getLogger("api.providers")


@blueprint.route("/providers/max_spots", methods=["POST", ])
@root_auth
@validate()
def change_max_spot_limit(
        body: MaxSpotLimit
):
    session: Session = get_session()
    provider: Provider = session.scalar(select(Provider).where(Provider.id == body.id))
    if provider is None:
        raise exceptions.ProviderDoesntExist()
    provider.max_spots += body.value
    session.add(provider)
    session.commit()
    return provider.dict()


__all__ = [
    "blueprint",
]
