from flask import Flask, render_template, request, redirect, url_for
from src.models.index_view_model import IndexViewModel
from src.mongo_config import MongoConfig
from src.mongo_db_client import MongoClient


def create_app():
    app = Flask(__name__)
    item_storage_client = MongoClient(MongoConfig())

    @app.route('/')
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

    return app


if __name__ == '__main__':
    create_app().run()
