__all__ = ["blueprint"]

from flask import request, Blueprint
from flask_login import login_required, login_user, current_user, user_unauthorized
from flask_pydantic import validate

from data import config, exceptions
from data.database import User
from data.database.db_session import get_session
from data.database.manager import get_manager
from data.datatypes import RegisterUser

import uuid
import json

from data.datatypes.users import UserListen


blueprint = Blueprint(
    "users",
    __name__,
)


@blueprint.route("/users", methods=["POST"])
@validate()
def create_user(body: RegisterUser) -> json:
    manager = get_manager()

    user = manager.create_user()
    return {
        "id": user.id,
        "listen_to": user.listen_to}

