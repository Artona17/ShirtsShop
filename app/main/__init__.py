from flask import Blueprint
# -*- coding: utf-8 -*-
main = Blueprint('main', __name__)
from . import views, errors

