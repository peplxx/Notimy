import json
from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy.orm import Session

from notimy.config.roles import Roles
from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider, User
from notimy.middleware.token_auth import root_auth
from notimy.schemas.providers import RegisterProvider

blueprint = Blueprint(
    "create_provider",
    __name__,
)
log = getLogger("api.providers")


@blueprint.route("/providers/new", methods=["POST", ])
@root_auth
@validate()
def create_provider(
        body: RegisterProvider
):
    session: Session = get_session()
    log.info(f"Registering provider {body.name}")
    provider_user = User(role=Roles.providerUser.value)
    session.add(provider_user)
    session.commit()

    provider = Provider(name=body.name, description=body.description, account=provider_user.id)
    session.add(provider)
    session.commit()
    provider_user.data = json.dumps({
        "token": provider.token
    })
    session.commit()
    log.info("Provider registered successfully!")
    return provider.dict()


__all__ = [
    "blueprint",
]
