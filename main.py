import json
import os
from flask import Flask, redirect, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pydantic import validate

from api.blueprints import blueprints
from data import config
from data.database import User
from data.database.db_session import get_session, global_init
from data.database.manager import init_manager, get_manager
from data.datatypes.users import UserListen

from logging.config import dictConfig
from logging import getLogger


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False

login_manager = LoginManager()
login_manager.init_app(app)
log = getLogger("main")

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html', title='Страница не найдена'), 404
@login_manager.user_loader
def load_user(user_id):  # find user in database
    db_sess = get_session()
    return db_sess.get(User, user_id)

@app.before_request
def track_previous_url():
    session['previous_url'] = session.get('current_url')
    session['current_url'] = request.url


@app.errorhandler(401)
def handle_unauthorized(error):
    # User is unauthorized so redirecting to login page
    log.debug("Unauthorized access from user -> redirecting to /login")
    return redirect("/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    user = current_user
    try:
        log.debug("User [id=%s] already exists!", user.id)
    except AttributeError:
        log.debug("Creating new user")
        manager = get_manager()
        user = manager.create_user()
        login_user(user, remember=True)
    previous_url = session.get('previous_url')
    log.debug(f"Redirecting to {previous_url}")
    return redirect(previous_url)


@app.route("/me", methods=["POST", "GET"])
@login_required
def show_user_info():
    log.debug("Accessing page /me [id=%s]", current_user.id)
    user = current_user
    return {
        "id": user.id,
        "listen_to": user.listen_to}


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    log.debug("Logging out user [id=%s]",current_user.id)
    logout_user()
    log.debug("Successfully logged out!")
    return {"message": "You successfully logged out."}


@app.route('/')
def index():
    log.debug("Index page!")
    return {"message": 'root'}


@app.route("/users", methods=["POST"])
@validate()
@login_required
def listen_a_channel(body: UserListen):
    # THIS FUNCTION IS OLD IMPLEMENTATION DO NOT READ
    manager = get_manager()
    manager.make_user_listen(current_user, body.channel)
    return {
        "message": "User connected to a new channel successfully"
    }

# @app.route("/get/", methods=[""])


if __name__ == '__main__':
    # Setting config for logger
    with open("data/logging.json") as logging_file:
        logging_config = json.load(logging_file)
    dictConfig(logging_config)
    log = getLogger("main")

    # Initializing database connection
    global_init(database=config.database_name,
                user=config.database_user,
                password=config.database_pass,
                host=config.database_host)
    init_manager()

    # Connecting all blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    log.info("Initialization complete, starting server")
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=port, debug=True)
