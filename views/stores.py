import json

from flask import Blueprint, render_template, request, redirect, url_for

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


@stores_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
def update_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.query = json.loads(request.form['query'])
        store.tag_name = request.form['tag_name']
        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@stores_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    Store.get_by_id(store_id).delete_from_mongo()
    return redirect(url_for('.index'))
