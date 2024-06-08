__all__ = ["blueprint"]

import pprint

from flask import Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database.manager import get_manager
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
    log.info("Provider registered successfully!")
    return {
        "id": provider.id,
        "token": provider.token
    }


@blueprint.route("/providers", methods=['PUT'])
@validate()
def update_providers_data(body: UpdateProviderData):
    log.info(f"Updating provider data [token={body.token}]")
    manager = get_manager()
    try:
        manager.update_provider(data=body)
        return {"message": "Data was successfully updated!"}
    except ValueError:
        raise exceptions.BadTokenException


@blueprint.route("/providers/spots", methods=['POST'])
@validate()
def register_provider_spot(body: ProviderAuth):
    log.debug("Registering new spot for provider [token=%s]", body.token)
    manager = get_manager()
    try:
        spot = manager.create_provider_spot(body.token)
        log.debug(spot.dict)
        d = spot.dict
        log.debug("Spot created!")
        return d
    except ValueError:
        raise exceptions.BadTokenException