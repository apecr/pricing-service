import json

from flask import Blueprint, render_template, request

from models.store import Store

stores_blueprint = Blueprint('stores', __name__)


@stores_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@stores_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_mongo()

    return render_template('stores/new_store.html')
