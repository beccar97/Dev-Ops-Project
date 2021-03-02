import os


class AuthConfig:
    def __init__(self):
        self.client_id = os.environ.get('GITHUB_AUTH_CLIENT_ID')
        self.client_secret = os.environ.get('GITHUB_AUTH_CLIENT_SECRET')
