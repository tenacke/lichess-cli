from __future__ import annotations

from lichess.api import RequestClient
from lichess.api import Session
from lichess.api import Token
from lichess import BaseClient
from lichess import CLIError

API_URL = "https://lichess.org"

class QueryClient(RequestClient):
    def init(self, base_url: str | None = None, token_key: str | None = None):
        client = BaseClient()
        self.set_credentials(client.get_credentials())

        if token_key is None:
            token_key = self.get_option('token', 'key')
            if token_key == '':
                raise CLIError(NameError("No token key provided. See 'lichess token --help' for more information."))
        
        token_handler = Token()
        self.token = token_handler.get(token_key)
        self.session = Session(self.token)

        super().init(session=self.session, base_url=base_url or API_URL)

