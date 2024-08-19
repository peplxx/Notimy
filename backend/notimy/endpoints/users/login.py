from logging import getLogger
from typing import Optional
from uuid import UUID

from flask import Blueprint, redirect, session, request
from flask_login import current_user, login_user
from sqlalchemy import select
from sqlalchemy.orm import Session

from frontend.data.db.connection import get_session
from frontend.data.db.models import User, Spot, Provider

log = getLogger("api.users")
blueprint = Blueprint(
    "user_login",
    __name__
)


def find_token_user(session: Session, token) -> UUID | None:
    if token is None:
        return None
    tables = [Spot, Provider]
    for table in tables:
        result = session.scalar(select(table).where(table.token == token))
        if result:
            return result.account
    return None


@blueprint.route("/login", methods=["GET", "POST"])
def login(
):
    token: Optional[str] = request.args.get('token')
    user = current_user
    db_sess = get_session()
    service_user_id = find_token_user(db_sess, token)
    if service_user_id is None:
        try:
            log.debug("User [id=%s] already exists!", user.id)
        except AttributeError:
            log.debug("Creating new user")

            user = User()
            db_sess.add(user)
            db_sess.commit()
            login_user(user, remember=True)
        if previous_url := session.get('previous_url'):
            log.debug(f"Redirecting to {previous_url}")
            return redirect(previous_url)
        return redirect("/api/me")

    user_instance = db_sess.scalar(select(User).where(User.id == service_user_id))
    login_user(user_instance, remember=True)
    return redirect("/api/me")
