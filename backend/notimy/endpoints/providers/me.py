from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider, Spot
from notimy.middleware.token_auth import get_token, provider_auth

blueprint = Blueprint(
    "get_provider",
    __name__,
)
log = getLogger("api.providers")



@blueprint.route("/providers/me",methods=["POST","GET"])
@provider_auth
@validate()
def get_provider(
):
    session: Session = get_session()
    token = get_token()
    provider = session.scalar(select(Provider).where(Provider.token == token))
    spots = [
        spot.dict() for spot in
        session.scalars(select(Spot).where(Spot.provider == provider.id))]
    response = provider.dict()
    response["spots_info"] = spots
    return response


__all__ = [
    "blueprint",
]