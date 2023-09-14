from __future__ import annotations

from utils.client import BaseClient
from utils.session import Session
from utils.exceptions import CLIError
from utils import tokens

from configparser import RawConfigParser


API_URL = "https://lichess.org"

class APIClient(BaseClient):
    def __init__(self, config:RawConfigParser, base_url: str | None = None, token_key: str | None = None):
        if token_key is None:
            token_key = config.get('token', 'key')
            if token_key == '':
                raise CLIError("No token key provided. See 'lichess token --help' for more information.")
        
        tokens.configure(config)
        self.token = tokens.get_token(token_key)
        self.session = Session(self.token)

        super().__init__(session=self.session, base_url=base_url or API_URL)

