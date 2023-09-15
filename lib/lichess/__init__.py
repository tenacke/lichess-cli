from __future__ import annotations

import os
from configparser import RawConfigParser
from argparse import Namespace
from gettext import gettext as _
from typing import Any, Dict, Tuple

from utils import Singleton, parse_config, parse_args

DEFAULT_HOME = os.path.expanduser('~/.lichess')

HOME = os.getenv('LICHESS_HOME')
if HOME is None:
    HOME = DEFAULT_HOME
ETC = os.path.join(HOME, 'etc')
MAN = os.path.join(HOME, 'share', 'mann')


class BaseClient(Singleton):
    def init(self, config: RawConfigParser | None = None, args: Namespace | None = None) -> None:
        self.set_credentials(config or parse_config(), args or parse_args())

    def new(self, config: RawConfigParser | None = None, args: Namespace | None = None) -> None:
        self.config = config or self.config
        self.args = args or self.args

    def set_credentials(self, config: RawConfigParser | None = None, args: Namespace | None = None) -> None:
        self.config = config
        self.args = args

    def get_credentials(self) -> Tuple[RawConfigParser, Namespace]:
        return self.config, self.args

    def has_section(self, section: str) -> bool:
        return self.config.has_section(section)
    
    def has_option(self, section: str, option: str) -> bool:
        return self.config.has_option(section, option)
    
    def add_section(self, section: str) -> None:
        self.config.add_section(section)

    def set_option(self, section: str, option: str, value: str) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_section(self, section: str) -> Dict[str, str]:
        if not self.config.has_section(section):
            raise KeyError(f'Section {section} not found')
        return dict(self.config.items(section))

    def get_option(self, section: str, option: str) -> str:
        if not self.config.has_option(section, option):
            raise KeyError(f'Option {option} not found in section {section}')
        return self.config.get(section, option)
    
    def get_argument(self, argument: str) -> Any:
        if not hasattr(self.args, argument):
            raise KeyError(f'Argument {argument} not found')
        return getattr(self.args, argument)
    

class BaseCommand(Singleton):
    def init(self, client: BaseClient) -> None:
        self.client = client
