from flask_login import LoginManager

from frontend.data.db.connection import get_session
from frontend.data.db.models import User

login_manager = LoginManager()
login_manager.remember_cookie_samesite = 'None'  # Set SameSite attribute for remember cookies
login_manager.remember_cookie_secure = True  # Set to True when using HTTPS

@login_manager.user_loader
def load_user(user_id):  # find user in database
    session = get_session()
    user = session.get(User, user_id)
    return user


__all__ = [
    "login_manager",
]