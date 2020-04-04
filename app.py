from flask import Flask, render_template, request

from views.alerts import alerts_blueprint
from views.items import item_blueprint

app = Flask(__name__)
app.register_blueprint(item_blueprint, url_prefix="/items")
app.register_blueprint(alerts_blueprint, url_prefix="/alerts")


if __name__ == '__main__':
    app.run(debug=True, port=4999)
