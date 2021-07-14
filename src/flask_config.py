import os


class FlaskConfig:
    def __init__(self):
        self.secret_key = os.environ.get('FLASK_SECRET_KEY').strip()
        self.login_disabled = os.environ.get('FLASK_LOGIN_DISABLED', False)
        self.log_level = os.environ.get('FLASK_LOG_LEVEL', 'ERROR')
        self.loggly_token = os.environ.get('LOGGLY_TOKEN', '').strip()
