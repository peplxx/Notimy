from flask import json, Blueprint
from werkzeug.exceptions import HTTPException

blueprint = Blueprint(
    "errors",
    __name__,
)


@blueprint.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
