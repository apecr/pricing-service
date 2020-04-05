from flask import Blueprint, render_template, request, url_for, redirect

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
        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        Alert(name=alert_name, item_id=item._id, price_limit=price_limit).save_to_mongo()
    return render_template('alerts/new_alert.html')


@alerts_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def update_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('.show_all_alerts'))
    return render_template('alerts/edit_alert.html', alert=alert)
