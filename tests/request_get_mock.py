import json
from src.trello_config import TrelloConfig
from datetime import datetime, timedelta


class RequestGetMock:
    def __init__(self):
        self.config = TrelloConfig()

        yesterday = (datetime.now() - timedelta(days=1)).isoformat()

        self.fake_get_list_data = [
            {
                "id": "todo-list-id",
                "name": "To Do",
                "closed": False,
                "pos": 65535,
                "softLimit": None,
                "idBoard": "idBoard",
                "subscribed": False,
                "cards": [
                    {
                        "id": "todo-item-id",
                        "checkItemStates": None,
                        "closed": False,
                        "dateLastActivity": yesterday,
                        "desc": "",
                        "descData": None,
                        "dueReminder": None,
                        "idBoard": "idBoard",
                        "idList": "todo-list-id",
                        "idMembersVoted": [],
                        "idShort": 5,
                        "idAttachmentCover": None,
                        "idLabels": [],
                        "manualCoverAttachment": False,
                        "name": "TO DO ITEM",
                        "pos": 65536,
                        "shortLink": "JAJHnCXe",
                        "isTemplate": False,
                        "badges": {
                            "attachmentsByType": {
                                "trello": {
                                    "board": 0,
                                    "card": 0
                                }
                            },
                            "location": False,
                            "votes": 0,
                            "viewingMemberVoted": False,
                            "subscribed": False,
                            "fogbugz": "",
                            "checkItems": 0,
                            "checkItemsChecked": 0,
                            "checkItemsEarliestDue": None,
                            "comments": 0,
                            "attachments": 0,
                            "description": False,
                            "due": None,
                            "dueComplete": False
                        },
                        "dueComplete": False,
                        "due": None,
                        "idChecklists": [],
                        "idMembers": [],
                        "labels": [],
                        "shortUrl": "todo-item-shortUrl",
                        "subscribed": False,
                        "url": "todo-item-url",
                        "cover": {
                            "idAttachment": None,
                            "color": None,
                            "idUploadedBackground": None,
                            "size": "normal",
                            "brightness": "light"
                        }
                    }
                ]
            },
            {
                "id": "doing-list-id",
                "name": "Doing",
                "closed": False,
                "pos": 131071,
                "softLimit": None,
                "idBoard": "idBoard",
                "subscribed": False,
                "cards": [
                    {
                        "id": "doing-item-id",
                        "checkItemStates": None,
                        "closed": False,
                        "dateLastActivity": yesterday,
                        "desc": "",
                        "descData": None,
                        "dueReminder": None,
                        "idBoard": "idBoard",
                        "idList": "doing-list-id",
                        "idMembersVoted": [],
                        "idShort": 4,
                        "idAttachmentCover": None,
                        "idLabels": [],
                        "manualCoverAttachment": False,
                        "name": "DOING ITEM",
                        "pos": 49152,
                        "shortLink": "SJ6lzZpY",
                        "isTemplate": False,
                        "badges": {
                            "attachmentsByType": {
                                "trello": {
                                    "board": 0,
                                    "card": 0
                                }
                            },
                            "location": False,
                            "votes": 0,
                            "viewingMemberVoted": False,
                            "subscribed": False,
                            "fogbugz": "",
                            "checkItems": 0,
                            "checkItemsChecked": 0,
                            "checkItemsEarliestDue": None,
                            "comments": 0,
                            "attachments": 0,
                            "description": False,
                            "due": None,
                            "dueComplete": False
                        },
                        "dueComplete": False,
                        "due": None,
                        "idChecklists": [],
                        "idMembers": [],
                        "labels": [],
                        "shortUrl": "doing-item-short-url",
                        "subscribed": False,
                        "url": "doing-item-short-url",
                        "cover": {
                            "idAttachment": None,
                            "color": None,
                            "idUploadedBackground": None,
                            "size": "normal",
                            "brightness": "light"
                        }
                    }
                ]
            },
            {
                "id": "done-list-id",
                "name": "Done",
                "closed": False,
                "pos": 196607,
                "softLimit": None,
                "idBoard": "idBoard",
                "subscribed": False,
                "cards": [
                    {
                        "id": "done-item-id",
                        "checkItemStates": None,
                        "closed": False,
                        "dateLastActivity": yesterday,
                        "desc": "",
                        "descData": None,
                        "dueReminder": None,
                        "idBoard": "idBoard",
                        "idList": "done-list-id",
                        "idMembersVoted": [],
                        "idShort": 3,
                        "idAttachmentCover": None,
                        "idLabels": [],
                        "manualCoverAttachment": False,
                        "name": "DONE ITEM",
                        "pos": 32768,
                        "shortLink": "7XHMwOj2",
                        "isTemplate": False,
                        "badges": {
                            "attachmentsByType": {
                                "trello": {
                                    "board": 0,
                                    "card": 0
                                }
                            },
                            "location": False,
                            "votes": 0,
                            "viewingMemberVoted": False,
                            "subscribed": False,
                            "fogbugz": "",
                            "checkItems": 0,
                            "checkItemsChecked": 0,
                            "checkItemsEarliestDue": None,
                            "comments": 0,
                            "attachments": 0,
                            "description": False,
                            "due": None,
                            "dueComplete": False
                        },
                        "dueComplete": False,
                        "due": None,
                        "idChecklists": [],
                        "idMembers": [],
                        "labels": [],
                        "shortUrl": "done-item-short-url",
                        "subscribed": False,
                        "url": "done-item-url",
                        "cover": {
                            "idAttachment": None,
                            "color": None,
                            "idUploadedBackground": None,
                            "size": "normal",
                            "brightness": "light"
                        }
                    },
                ]
            }
        ]

    def mock_get_requests(self, url, params):
        class MockRequestGetResponse:
            def __init__(self, data, status_code):
                self.data = data
                self.status_code = status_code

            def json(self):
                return self.data

        if url == "%s/members/me/boards" % self.config.base_url:
            return {
                # fake board response
            }
        elif url == '%s/boards/%s/lists' % (self.config.base_url, self.config.board_id):
            response = MockRequestGetResponse(self.fake_get_list_data, 200)
            return response
