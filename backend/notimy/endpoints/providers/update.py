from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider
from notimy.middleware.token_auth import get_token, provider_auth
from notimy.schemas.providers import UpdateProviderData

blueprint = Blueprint(
    "update_provider",
    __name__,
)
log = getLogger("api.providers")


@blueprint.route("/providers/update", methods=["PUT", ])
@provider_auth
@validate()
def update_provider(
        body: UpdateProviderData
):
    session: Session = get_session()
    token = get_token()

    provider: Provider = session.scalar(
        select(Provider).where(Provider.token == token)
    )
    if body.name:
        provider.name = body.name
    if body.description:
        provider.description = body.description
    session.commit()
    log.info("Provider updated successfully!")
    return provider.dict()


__all__ = [
    "blueprint",
]
