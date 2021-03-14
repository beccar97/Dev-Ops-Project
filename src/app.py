import requests
from flask import Flask, redirect, render_template, url_for, current_app, request
from flask_login import LoginManager, login_required, login_user, current_user
from functools import wraps
from oauthlib.oauth2 import WebApplicationClient
from src.auth_config import AuthConfig
from src.flask_config import FlaskConfig
from src.models.index_view_model import IndexViewModel
from src.mongo_config import MongoConfig
from src.mongo_db_client import MongoClient
from src.user import User, UserRole, AnonymousUser


def create_app():
    app = Flask(__name__)
    flask_config = FlaskConfig()
    app.secret_key = flask_config.secret_key

    item_storage_client = MongoClient(MongoConfig())

    auth_config = AuthConfig()
    login_manager = LoginManager()

    if flask_config.login_disabled:
        app.config['LOGIN_DISABLED'] = True
        login_manager.anonymous_user = AnonymousUser

    oauth_client = WebApplicationClient(auth_config.client_id)

    @app.route('/')
    @login_required
    def index():
        items = item_storage_client.get_items()
        view_model = IndexViewModel(items)
        return render_template('index.html', view_model=view_model)

    @app.route('/items/new', methods=['POST'])
    @login_required
    @write_required
    def add_item():
        name = request.form['name']
        item_storage_client.add_item(name)
        return redirect(url_for('index'))

    @app.route('/items/<id>/start')
    @login_required
    @write_required
    def start_item(id):
        item_storage_client.start_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/complete')
    @login_required
    @write_required
    def complete_item(id):
        item_storage_client.complete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/uncomplete')
    @login_required
    @write_required
    def uncomplete_item(id):
        item_storage_client.uncomplete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/delete')
    @login_required
    @write_required
    def delete_item(id):
        item_storage_client.delete_item(id)
        return redirect(url_for('index'))

    @app.route('/login/callback')
    def login():
        oauth_client.parse_request_uri_response(request.full_path)
        url, headers, body = oauth_client.prepare_token_request(
            auth_config.access_token_url, client_secret=auth_config.client_secret)
        access_token = requests.post(url, headers=headers, data=body).text

        oauth_client.parse_request_body_response(access_token)
        url, headers, body = oauth_client.add_token(auth_config.user_info_url)
        user_info = requests.get(url, headers=headers)
        user = User(user_info.json()['id'])
        login_user(user)

        return redirect(url_for('index'))

    @login_manager.unauthorized_handler
    def unauthenticated():
        # TODO: Add a state parameter to prevent CSRF
        uri = oauth_client.prepare_request_uri(auth_config.authorization_url)
        return redirect(uri)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    return app


def write_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user
        if user.role() != UserRole.WRITER:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


if __name__ == '__main__':
    create_app().run()
