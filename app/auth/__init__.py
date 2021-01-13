from flask import Blueprint, current_app

auth = Blueprint('auth', __name__)

from . import views
from ..models import User