__all__ = ["blueprint"]

from flask import request, Blueprint
from flask_pydantic import validate

from data import config, exceptions
from data.database import User
from data.database.db_session import get_session
from data.datatypes import RegisterUser

import uuid
import json
import requests

blueprint = Blueprint(
    "users",
    __name__,
)


@blueprint.route("/users", methods=["POST"])
@validate()
def create_user(body: RegisterUser) -> json:
    user_uuid: str = str(uuid.uuid4())

    session: Session = get_session()
    user: User = session.query(User).filter(User.uuid == user_uuid).first()
    if user:
        return {
            "id": user.id,
            "listen_to": user.listen_to
        }
    new_user = User(uuid=user_uuid, listen_to=body.listen_to)
    session.add(new_user)
    session.commit()
    return {
        "id": new_user.id,
        "listen_to": new_user.listen_to
    }

@blueprint.route("/users", methods=["PUT"])
@validate()
def update_users_data(body: RegisterUser):
    session: Session = get_session()
    user = session.query(User).filter(User.id == body.id).first()
    if not user:
        return exceptions.BadTokenException
    user.listen_to = body.listen_to
    session.commit()
    return {
        "message": "User connected to a new channel successfully"
    }