from api.providers.routes import blueprint as provider_blueprint
from api.error_handling import blueprint as error_blueprint
from api.channels.routes import blueprint as channels_blueprint
from api.users.routes import blueprint as users_blueprint

blueprints = [provider_blueprint, error_blueprint, channels_blueprint, users_blueprint]
__all__ = ["blueprints", *blueprints]
