__all__ = ["blueprint"]

from flask import request, Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import User
from data.database.db_session import get_session

blueprint = Blueprint(
    "providers",
    __name__,
)


@blueprint.route("/providers", methods=["POST"])
@validate()