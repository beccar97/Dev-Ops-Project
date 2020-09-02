from src.models.todo_item import Item
import requests
from src.trello_config import TrelloConfig


class TrelloClient:
    def __init__(self, trello_config: TrelloConfig):
        self.trello_config = trello_config

    def get_auth_params(self):
        return {'key': self.trello_config.api_key, 'token': self.trello_config.api_secret}

    def build_url(self, endpoint):
        return self.trello_config.base_url + endpoint

    def build_params(self, params={}):
        full_params = self.get_auth_params()
        full_params.update(params)
        return full_params

    def create_board(self, name='Trello Board'):
        """
        Creates a new trello board with the given name.

        Args:
            name (str): The name of the board.

        Returns:
            id: The id of the created board.
        """

        params = self.build_params({'name': name})
        url = self.build_url('/boards')

        response = requests.post(url, params=params)
        board = response.json()

        return board['id']

    def delete_board(self, board_id):
        """
        Deletes the trello board with the given id.

        Args:
            name (str): The id of the board to be deleted.

        Returns:
            None
        """
        params = self.build_params()
        url = self.build_url('/boards/%s' % board_id)

        requests.delete(url, params=params)

    def get_lists(self):
        """
        Fetches all lists for the default Trello board.

        Returns:
            list: The list of Trello lists.
        """
        params = self.build_params(
            {'cards': 'open'})  # Only return cards that have not been archived
        url = self.build_url('/boards/%s/lists' % self.trello_config.board_id)

        response = requests.get(url, params=params)
        lists = response.json()

        return lists

    def get_list(self, name):
        """
        Fetches the list from Trello with the specified name.

        Args:
            name (str): The name of the list.

        Returns:
            list: The list and its items (cards), or None if no list matches the specified name.
        """
        lists = self.get_lists()
        return next((list for list in lists if list['name'] == name), None)

    def get_items(self):
        """
        Fetches all items (known as "cards") from Trello.

        Returns:
            list: The list of saved items.
        """
        lists = self.get_lists()

        items = []
        for card_list in lists:
            for card in card_list['cards']:
                items.append(Item.from_trello_card(card, card_list))

        return items

    def get_item(self, id):
        """
        Fetches the item ("card") with the specified ID.

        Args:
            id (str): The ID of the item.

        Returns:
            item: The item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item['id'] == id), None)

    def add_item(self, name):
        """
        Adds a new item with the specified name as a Trello card.

        Args:
            name (str): The name of the item.

        Returns:
            item: The saved item.
        """
        todo_list = self.get_list('To Do')

        params = self.build_params({'name': name, 'idList': todo_list['id']})
        url = self.build_url('/cards')

        response = requests.post(url, params=params)
        card = response.json()

        return Item.from_trello_card(card, todo_list)

    def start_item(self, id):
        """
        Moves the item with the specified ID to the "Doing" list in Trello.

        Args:
            id (str): The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        doing_list = self.get_list('Doing')
        card = self.move_card_to_list(id, doing_list)

        return Item.from_trello_card(card, doing_list)

    def complete_item(self, id):
        """
        Moves the item with the specified ID to the "Done" list in Trello.

        Args:
            id (str): The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        done_list = self.get_list('Done')
        card = self.move_card_to_list(id, done_list)

        return Item.from_trello_card(card, done_list)

    def uncomplete_item(self, id):
        """
        Moves the item with the specified ID to the "Doing" list in Trello.

        Args:
            id (str): The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        todo_list = self.get_list('Doing')
        card = self.move_card_to_list(id, todo_list)

        return Item.from_trello_card(card, todo_list)

    def move_card_to_list(self, card_id, list):
        params = self.build_params({'idList': list['id']})
        url = self.build_url('/cards/%s' % card_id)

        response = requests.put(url, params=params)
        card = response.json()

        return card

    def delete_item(self, card_id):
        """
        Deletes the item with the specified ID

        Args:
            id (str): The ID of the item.
        """
        params = self.build_params()
        url = self.build_url('/cards/%s' % card_id)

        requests.delete(url, params=params)
