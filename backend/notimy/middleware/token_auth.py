from functools import wraps

from flask import request
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask_login import current_user
from notimy.config import config
from notimy.data.db.connection import get_session
from notimy.data.db.models import Provider, Spot, User
from notimy.utils import exceptions


def get_token() -> str:
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    elif request.data and request.json.get('token'):
        token = request.json['token']
    else:
        try:  # Get token from user.data
            user: User = current_user
            user_data = user.get_data()
            token = user_data['token']
        except Exception:
            pass  # User is anonymous
    if not token:
        raise exceptions.BadTokenException
    return token


def token_validation(
        session: Session,
        base_class,
):
    token: str = get_token()
    result = session.scalar(
        select(base_class).where(base_class.token == token)
    )
    if not result:
        raise exceptions.BadTokenException


def spot_auth(fun):
    @wraps(fun)
    def wrapper(*args,
                session: Session = get_session()):
        token_validation(
            base_class=Spot,
            session=session
        )
        return fun(*args)

    return wrapper


def provider_auth(fun):
    @wraps(fun)
    def wrapper(*args,
                session: Session = get_session()):
        token_validation(
            base_class=Provider,
            session=session
        )
        return fun(*args)

    return wrapper


def root_auth(fun):
    @wraps(fun)
    def wrapper(*args):
        token: str = get_token()
        if token != config.ROOT_TOKEN:
            raise exceptions.BadTokenException
        return fun(*args)

    return wrapper
