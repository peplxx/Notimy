__all__ = ["blueprint"]

from flask import request, Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import Provider
from data.database.db_session import get_session
from data.datatypes import RegisterProvider, UpdateProviderData

blueprint = Blueprint(
    "providers",
    __name__,
)


@blueprint.route("/providers", methods=["POST"])
@validate()
def register_provider(body: RegisterProvider):
    if body.token != config.token:
        raise exceptions.BadTokenException
    session = get_session()
    provider = session.query(Provider).filter(
        Provider.name == body.name and Provider.description == body.description).first()
    if provider:
        return {
            "id": provider.id,
            "token": provider.token
        }
    new_provider = Provider(name=body.name, description=body.description)
    session.add(new_provider)
    session.commit()
    return {
        "id": new_provider.id,
        "token": new_provider.token
    }


@blueprint.route("/providers", methods=['PUT'])
@validate()
def update_providers_data(body: UpdateProviderData):
    session = get_session()
    provider = session.query(Provider).filter(Provider.token == body.token).first()
    if not provider:

        return exceptions.BadTokenException
    provider.name = body.name
    provider.description = body.description
    session.commit()
    return {"message": "Data was successfully updated!"}





