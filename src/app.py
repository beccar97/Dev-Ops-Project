from src.flask_config import FlaskConfig
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
from src.auth_config import AuthConfig
from src.models.index_view_model import IndexViewModel
from src.mongo_config import MongoConfig
from src.mongo_db_client import MongoClient
from src.user import User


def create_app():
    app = Flask(__name__)
    app.secret_key = FlaskConfig().secret_key

    item_storage_client = MongoClient(MongoConfig())

    auth_config = AuthConfig()
    login_manager = LoginManager()
    oauth_client = WebApplicationClient(auth_config.client_id)

    @app.route('/')
    @login_required
    def index():
        items = item_storage_client.get_items()
        view_model = IndexViewModel(items)
        return render_template('index.html', view_model=view_model)

    @app.route('/items/new', methods=['POST'])
    def add_item():
        name = request.form['name']
        item_storage_client.add_item(name)
        return redirect(url_for('index'))

    @app.route('/items/<id>/start')
    def start_item(id):
        item_storage_client.start_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/complete')
    def complete_item(id):
        item_storage_client.complete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/uncomplete')
    def uncomplete_item(id):
        item_storage_client.uncomplete_item(id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/delete')
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
        uri = oauth_client.prepare_request_uri(
            'https://github.com/login/oauth/authorize')
        return redirect(uri)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    return app


if __name__ == '__main__':
    create_app().run()
