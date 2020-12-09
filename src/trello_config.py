"""Trello API configuration."""
import os


class TrelloConfig:
    base_url = 'https://api.trello.com/1'

    def __init__(self):
        self.api_key = os.environ.get('TRELLO_API_KEY').strip()
        self.api_secret = os.environ.get('TRELLO_API_SECRET').strip()
        self.board_id = os.environ.get('TRELLO_BOARD_ID').strip()
