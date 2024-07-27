from json import load
from logging import getLogger
from logging.config import dictConfig
from notimy.config import config
from notimy.endpoints import blueprints
from notimy.middleware.login_manager import login_manager
from flask import Flask, session, request, redirect
from notimy.utils.json_encoder import UUIDEncoder

log = getLogger("main")


def get_app() -> Flask:
    global app
    if not app:
        buff = Flask(__name__)
        buff.config['SECRET_KEY'] = 'abcdef'
        buff.config['JSON_AS_ASCII'] = False
        for blueprint in blueprints:
            buff.register_blueprint(blueprint)
    return buff


def setup_logging() -> None:
    global log
    logging_config = load(open(f"{config.APP_NAME}/data/logging.json"))
    dictConfig(logging_config)
    log = getLogger("main")

app = None
app = get_app()


@app.before_request
def track_previous_url():
    session.permanent = True
    session['previous_url'] = session.get('current_url')
    session['current_url'] = request.url


@app.errorhandler(401)
def handle_unauthorized(error):
    log.debug("Unauthorized access from user -> redirecting to /login")
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def index():
    return {"message": "Hello, it is Notimy!"}


if __name__ == '__main__':
    # Setting config for logger
    setup_logging()
    login_manager.init_app(app)

    # app.run(host=CONFIG.APP_HOST, port=CONFIG.APP_PORT)
    app.run(port=config.APP_PORT, debug=True)
