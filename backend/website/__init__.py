from flask import Flask
from pathlib import Path
import os


SECRET_KEY_FILE = Path('secret_key')

def create_app():
    app = Flask(__name__)

    try:
        # try to load the secret key from the file
        secret_key = SECRET_KEY_FILE.read_bytes()
    except FileNotFoundError:
        # if none exists, create a new secret key and save it
        secret_key = os.urandom(16)
        SECRET_KEY_FILE.write_bytes(secret_key)
    app.secret_key = secret_key

    from .views import views
    app.register_blueprint(views)

    from .quinn.views import views as quinn_views
    app.register_blueprint(quinn_views)

    from .greg.views import views as greg_views
    app.register_blueprint(greg_views)


    return app
