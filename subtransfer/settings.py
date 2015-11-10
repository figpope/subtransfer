import os
import json

CLIENT_ID = ''
CLIENT_SECRET = ''
HOST = 'http://127.0.0.1:65010'
REDIRECT_URI = '/authorize_callback'
USER_AGENT = 'SubTransfer, a tool to transfer subreddit subscriptions from one account to another'

_settings_locals = locals()


def update_config_from_json(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            _settings_locals.update(json.loads(json_file.read()))

update_config_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'))