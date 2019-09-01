from flask import Blueprint

receipt_blueprint = Blueprint('receipt', __name__, template_folder='templates', \
    static_folder='static')

from . import routes


