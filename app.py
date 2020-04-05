from flask import Flask

from views.alerts import alerts_blueprint
from views.stores import stores_blueprint

app = Flask(__name__)
app.register_blueprint(alerts_blueprint, url_prefix="/alerts")
app.register_blueprint(stores_blueprint, url_prefix='/stores')


if __name__ == '__main__':
    app.run(debug=True, port=4999)
