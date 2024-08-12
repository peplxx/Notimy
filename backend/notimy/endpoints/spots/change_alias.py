from logging import getLogger

from flask import Blueprint
from flask_pydantic import validate
from sqlalchemy import select
from sqlalchemy.orm import Session

from notimy.config import config
from notimy.data.db.connection import get_session
from notimy.data.db.models import Spot, Alias
from notimy.middleware import spot_auth
from notimy.middleware.token_auth import get_token
from notimy.schemas.spots import ChangeAlias
from notimy.services.spot.logic import get_spot_by_id
from notimy.utils.exceptions import WrongAliasNameSize, AliasIsTaken

log = getLogger("api.spots")

blueprint = Blueprint(
    'change_alias',
    __name__
)


@blueprint.route("/spots/change_alias", methods=["POST"])
@spot_auth
@validate()
def change_alias(
       body: ChangeAlias,
):
    token: str = get_token()
    session: Session = get_session()
    if len(body.name) != config.ALIAS_NAME_SIZE:
        raise WrongAliasNameSize()

    already_exist = session.scalar(select(Alias).where(Alias.name == body.name))
    if already_exist:
        raise AliasIsTaken()

    spot = session.scalar(select(Spot).where(Spot.token == token))
    spot_id = spot.id
    alias = session.scalar(select(Alias).where(Alias.base == spot_id))
    alias.name = body.name
    session.commit()
    return get_spot_by_id(session, spot_id)
