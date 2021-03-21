import requests
import secrets
from flask import Flask, redirect, render_template, url_for, request, session, Response
from flask_login import LoginManager, login_required, login_user, current_user
from functools import wraps
from oauthlib.oauth2 import WebApplicationClient
from src.auth_config import AuthConfig
from src.flask_config import FlaskConfig
from src.models.index_view_model import IndexViewModel
from src.mongo_config import MongoConfig
from src.mongo_db_client import MongoClient
from src.models.user import User, UserRole, AnonymousUser


def create_app():
    app = Flask(__name__)
    flask_config = FlaskConfig()
    app.secret_key = flask_config.secret_key

    storage_client = MongoClient(MongoConfig())

    auth_config = AuthConfig()
    login_manager = LoginManager()

    if flask_config.login_disabled:
        app.config['LOGIN_DISABLED'] = True
        login_manager.anonymous_user = AnonymousUser

    oauth_client = WebApplicationClient(auth_config.client_id)

    @app.route('/')
    @login_required
    def index():
        items = storage_client.get_items()
        view_model = IndexViewModel(items)
        return render_template('index.html', view_model=view_model)

    @app.route('/items/new', methods=['POST'])
    @login_required
    @write_required
    def add_item():
        name = request.form['name']
        storage_client.add_item(name)
        return redirect(url_for('index'))

    @app.route('/items/<id>/start')
    @login_required
    @write_required
    def start_item(id):
        storage_client.start_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/complete')
    @login_required
    @write_required
    def complete_item(id):
        storage_client.complete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/uncomplete')
    @login_required
    @write_required
    def uncomplete_item(id):
        storage_client.uncomplete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/delete')
    @login_required
    @write_required
    def delete_item(id):
        storage_client.delete_item(id)
        return redirect(url_for('index'))

    @app.route('/login/callback')
    def login():
        state = session['state']
        oauth_client.parse_request_uri_response(request.full_path, state=state)
        url, headers, body = oauth_client.prepare_token_request(
            auth_config.access_token_url,
            state=state,
            client_secret=auth_config.client_secret
        )
        access_token = requests.post(url, headers=headers, data=body).text

        oauth_client.parse_request_body_response(access_token)
        url, headers, body = oauth_client.add_token(auth_config.user_info_url)
        user_info = requests.get(url, headers=headers)

        user = storage_client.get_or_add_user(user_info.json()['id'])
        login_user(user)

        return redirect(url_for('index'))

    @login_manager.unauthorized_handler
    def unauthenticated():
        state = secrets.token_hex(16)
        session['state'] = state
        uri = oauth_client.prepare_request_uri(
            auth_config.authorization_url, state=state)
        return redirect(uri)

    @login_manager.user_loader
    def load_user(user_id):
        return storage_client.get_user(user_id)

    login_manager.init_app(app)

    return app


def write_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user
        if not user.has_write_permissions():
            return Response('You are not authorised to perform this action', 401)
        return f(*args, **kwargs)
    return decorated_function


if __name__ == '__main__':
    create_app().run()
