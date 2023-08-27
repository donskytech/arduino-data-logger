from flask import Blueprint

commands_bp = Blueprint('commands', __name__)

from . import views