__all__ = ["blueprint"]

from flask import Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import Provider
from data.database.db_session import get_session
from data.database.manager import DatabaseManager, get_manager
from data.datatypes import RegisterProvider, UpdateProviderData

blueprint = Blueprint(
    "providers",
    __name__,
)


@blueprint.route("/providers", methods=["POST"])
@validate()
def register_provider(body: RegisterProvider):
    manager = get_manager()
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





