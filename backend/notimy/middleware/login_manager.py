from flask_login import LoginManager

from notimy.data.db.connection import get_session
from notimy.data.db.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):  # find user in database
    session = get_session()
    user = session.get(User, user_id)
    return user


__all__ = [
    "login_manager",
]