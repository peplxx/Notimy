__all__ = ["blueprint"]

from flask import request, Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import User
from data.database.db_session import get_session

blueprint = Blueprint(
    "users",
    __name__,
)


@blueprint.route("/users", methods=["POST"])
@validate()
async def create_user():
    pass