from flask import Blueprint, render_template, request, url_for, redirect, session

from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login

alerts_blueprint = Blueprint('alerts', __name__)


@alerts_blueprint.route('/')
@requires_login
def show_all_alerts():
    print(session['email'])
    alerts = Alert.find_many_by('user_email', session['email'])
    for alert in alerts:
        print(alert)
    return render_template('alerts/index.html', alerts=alerts)


@alerts_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        Alert(name=alert_name, item_id=item._id, price_limit=price_limit, user_email=session['email'])\
            .save_to_mongo()
    return render_template('alerts/new_alert.html')


@alerts_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def update_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('.show_all_alerts'))
    return render_template('alerts/edit_alert.html', alert=alert)


@alerts_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.delete_from_mongo()
    return redirect(url_for('.show_all_alerts'))
