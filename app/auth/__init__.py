from flask import Blueprint

# defining a blueprint
auth = Blueprint('auth', __name__)

from . import views