import os

from dotenv import load_dotenv
from flask import Flask

from libs.mailgun import Mailgun
from views.alerts import alerts_blueprint
from views.stores import stores_blueprint
from views.users import user_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(ADMIN=os.environ.get('ADMIN'))

load_dotenv()
print(Mailgun.send_email(["alberto.eyo@gmail.com"], "Hello", "This is a test email", "<p>This is a HTML test.</p>"))

app.register_blueprint(alerts_blueprint, url_prefix="/alerts")
app.register_blueprint(stores_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=True, port=4999)
