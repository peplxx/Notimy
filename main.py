import os
from datetime import datetime
import random
from multiprocessing import Process
from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from api.blueprints import blueprints
from data import config, exceptions
from data.database import Provider, Channel, User
from data.database.db_session import get_session, global_init
from data.config import database_pass, database_user, database_name, database_host
from data.datatypes import RegisterProvider, ChanelCreation, Message, UpdateProviderData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


# @app.errorhandler(404)
# def not_found(error):  # Error/home/hellboy4/hellboyAcerman/Notimy/.venv/bin/python3 404
#     return render_template('404.html', title='Страница не найдена'), 404

@app.route('/')
def index():
    return {"message": 'root'}


if __name__ == '__main__':
    global_init(database=config.database_name,
                user=config.database_user,
                password=config.database_pass,
                host=config.database_host)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=port, debug=True)
