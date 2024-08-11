from json import load
from logging import getLogger
from logging.config import dictConfig
from flask_cors import CORS

from flask import Flask, redirect, request, session

from notimy.config import config
from notimy.endpoints import blueprints
from notimy.middleware.login_manager import login_manager

log = getLogger("main")


def get_app() -> Flask:
    global app
    if not app:
        buff = Flask(__name__)
        buff.config['SECRET_KEY'] = 'abcdef'
        buff.config['JSON_AS_ASCII'] = False
        buff.config['SESSION_COOKIE_SAMESITE'] = 'None'
        buff.config['SESSION_COOKIE_SECURE'] = True  # Set to True when using HTTPS
        # buff.config['REMEMBER_TOKEN_COOKIE_SAMESITE'] = 'None'
        # buff.config['REMEMBER_TOKEN_COOKIE_SECURE'] = True  # Set to True when using HTTPS
        for blueprint in blueprints:
            buff.register_blueprint(blueprint, url_prefix=config.API_PREFIX)
        CORS(buff, supports_credentials=True)
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
    return redirect("/api/login")




@app.route("/", methods=["GET", "POST"])
def index():
    return {"message": "Hello, it is Notimy!"}




if __name__ == '__main__':
    # Setting config for logger
    setup_logging()
    login_manager.init_app(app)
    # app.run(host=CONFIG.APP_HOST, port=CONFIG.APP_PORT)
    # app.config.update(
    # SESSION_COOKIE_SAMESITE='None',  # Allow cookies to be sent cross-site
    # SESSION_COOKIE_SECURE=True,      # Cookies are only sent over HTTPS
    # REMEMBER_COOKIE_SAMESITE='None',
    # REMEMBER_COOKIE_SECURE=True,
    # )
    # app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
    # app.config['REMEMBER_COOKIE_SECURE'] = True  # Set to False if not using HTTPS
    app.run(host="0.0.0.0", port=config.APP_PORT, ssl_context='adhoc')
