from api.providers.routes import blueprint as provider_blueprint
from api.error_handling import blueprint as error_blueprint
from api.channels.routes import blueprint as channels_blueprint

blueprints = [provider_blueprint, error_blueprint, channels_blueprint]
__all__ = ["blueprints", *blueprints]
