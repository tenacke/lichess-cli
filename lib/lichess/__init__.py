from __future__ import annotations

import os
from configparser import RawConfigParser, ConfigParser, ParsingError
from argparse import ArgumentParser, Namespace, _MutuallyExclusiveGroup, Action, HelpFormatter
from json import load, JSONDecodeError
from gettext import gettext as _
from typing import Iterable, Any, Dict

from utils.exceptions import CorruptedSourceError

DEFAULT_HOME = os.path.expanduser('~/.lichess')

HOME = os.getenv('LICHESS_HOME')
if HOME is None:
    HOME = DEFAULT_HOME
ETC = os.path.join(HOME, 'etc')
MAN = os.path.join(HOME, 'share', 'mann')


class Singleton:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Singleton:
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance
    
    def init(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError('This method must be implemented in the subclass')


class BaseFormatter(HelpFormatter):
    def _format_usage(self, usage: str | None, actions: Iterable[Action], groups: Iterable[_MutuallyExclusiveGroup], prefix: str | None) -> str:
        if prefix is None:
            prefix = _('Usage: ')
        return super()._format_usage(usage, actions, groups, prefix)
    

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        return ''.join(indent + line for line in text.splitlines(keepends=True))

    def _split_lines(self, text: str, width: int) -> list[str]:
        if '\n' in text:
            return text.splitlines()
        return super()._split_lines(text, width)
    

class MainFormatter(BaseFormatter):
    pass


class SubcommandFormatter(BaseFormatter):
    pass


def parse_config() -> RawConfigParser:
    config = ConfigParser(inline_comment_prefixes=('#', ';'))
    
    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        if os.path.isfile(os.path.join(ETC, 'defaults.conf')):
            config.read(os.path.join(ETC, 'defaults.conf'))
        else:
            raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {os.path.join(ETC, "defaults.conf")} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
        
        if os.path.isfile(os.path.join(ETC, 'lichess.conf')):
            config.read(os.path.join(ETC, 'lichess.conf'))
    except ParsingError as e:
        e.message = f'Error parsing configuration file {e.source}:\n{e.message}'
        raise CorruptedSourceError(e)

    return config

def parse_args() -> Namespace:
    def set_subparser(parser: Any, parser_dict: Dict[str, Any]) -> None:
        subparsers = parser.add_subparsers(**parser_dict['kwargs'])
        for subparser_dict in parser_dict['subparsers']:
            subparser = subparsers.add_parser(**subparser_dict['kwargs'], formatter_class=SubcommandFormatter)
            if subparser_dict['parser_type'] == 'subparser':
                set_subparser(subparser, subparser_dict['subparser'])
            elif subparser_dict['parser_type'] == 'argument':
                set_argument(subparser, subparser_dict['args'])
    
    def set_argument(parser: Any, arguments: Dict[str, Any]) -> None:
        for argument_dict in arguments:
            parser.add_argument(*argument_dict['name'], **argument_dict['kwargs'])

    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    parser_file = os.path.join(ETC, 'parser.json')
    if not os.path.isfile(parser_file):
        raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {parser_file} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        parser_dict = load(open(parser_file, 'r'))
    except JSONDecodeError as e:
        raise CorruptedSourceError(e)

    parser = ArgumentParser(**parser_dict['kwargs'], formatter_class=BaseFormatter)
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()


class BaseClient(Singleton):
    def init(self, config: RawConfigParser | None = None, args: Namespace | None = None) -> None:
        self.config = config or parse_config()
        self.args = args or parse_args()

    def has_section(self, section: str) -> bool:
        return self.config.has_section(section)
    
    def has_option(self, section: str, option: str) -> bool:
        return self.config.has_option(section, option)
    
    def add_section(self, section: str) -> None:
        self.config.add_section(section)

    def set_option(self, section: str, option: str, value: str) -> None:
        self.config.set(section, option, value)

    def get_section(self, section: str) -> Dict[str, str]:
        return dict(self.config.items(section))

    def get_option(self, section: str, option: str) -> str:
        return self.config.get(section, option)
    
    def get_command(self) -> str:
        return self.get_argument('command')
    
    def get_subcommand(self) -> str | None:
        return self.get_argument('subcommand')
    
    def get_argument(self, argument: str) -> Any:
        return getattr(self.args, argument)

    def get_config(self) -> RawConfigParser:
        return self.config
    
    def get_args(self) -> Namespace:
        return self.args
    
