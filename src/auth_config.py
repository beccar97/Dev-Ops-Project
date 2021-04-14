import os


class AuthConfig:
    authorization_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    user_info_url = 'https://api.github.com/user'
    def __init__(self):
        self.client_id = os.environ.get('GITHUB_AUTH_CLIENT_ID').strip()
        self.client_secret = os.environ.get('GITHUB_AUTH_CLIENT_SECRET').strip()
