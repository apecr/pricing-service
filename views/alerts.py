from flask import Blueprint, render_template, request

from models.alert import Alert
from models.item import Item
from models.store import Store

alerts_blueprint = Blueprint('alerts', __name__)


@alerts_blueprint.route('/')
def show_all_alerts():
    alerts = Alert.all()
    return render_template('alerts/index.html', alerts=alerts)


@alerts_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.save_to_mongo()

        Alert(item_id=item._id, price_limit=price_limit).save_to_mongo()
    return render_template('alerts/new_alert.html')

