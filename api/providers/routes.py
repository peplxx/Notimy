__all__ = ["blueprint"]

from flask import Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import Provider
from data.database.db_session import get_session
from data.database.manager import DatabaseManager, get_manager
from data.datatypes import RegisterProvider, UpdateProviderData, ProviderAuth
from logging import getLogger

blueprint = Blueprint(
    "providers",
    __name__,
)

log = getLogger("api.providers")


@blueprint.route("/providers", methods=["POST"])
@validate()
def register_provider(body: RegisterProvider):
    manager = get_manager()
    log.info(f"Registering provider {body.name}")
    if body.token != config.token:
        raise exceptions.BadTokenException
    provider = manager.register_provider(data=body)
    return {
        "id": provider.id,
        "token": provider.token
    }


@blueprint.route("/providers", methods=['PUT'])
@validate()
def update_providers_data(body: UpdateProviderData):
    manager = get_manager()
    try:
        manager.update_provider(data=body)
        return {"message": "Data was successfully updated!"}
    except ValueError as e:
        return exceptions.BadTokenException


@blueprint.route("/providers/spots", methods=['POST'])
@validate()
def register_provider_spot(body: ProviderAuth):
    log.debug(f"Registering spot for spot for provider [token=%s]", body.token)
    manager = get_manager()
    try:
        spot = manager.create_provider_spot(body.token)
        d = spot.dict
        log.debug(f"Spot created!")
        return d
    except ValueError:
        return exceptions.BadTokenException
