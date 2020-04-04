from flask import Blueprint

learning_blueprint = Blueprint('learning', __name__)


@learning_blueprint.route('/<string:name>')
def hello(name):
    return f"Hello {name}!"
