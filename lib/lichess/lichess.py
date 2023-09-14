#!/usr/bin/env python3

from __future__ import annotations

from argparse import _MutuallyExclusiveGroup, Action, ArgumentParser, HelpFormatter
from collections.abc import Iterable
from configparser import ConfigParser, ParsingError
from importlib import import_module
from json import load, JSONDecodeError
import os
import sys
import subprocess
from gettext import gettext as _

from utils.exceptions import LichessError, CorruptedSourceError
from . import HOME

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


def parse_config():
    config = ConfigParser(inline_comment_prefixes=('#', ';'))
    conf_dir = os.path.join(HOME, 'etc')
    
    if not os.path.exists(conf_dir):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {conf_dir} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        if os.path.isfile(os.path.join(conf_dir, 'defaults.conf')):
            config.read(os.path.join(conf_dir, 'defaults.conf'))
        else:
            raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {os.path.join(conf_dir, "defaults.conf")} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
        
        if os.path.isfile(os.path.join(conf_dir, 'lichess.conf')):
            config.read(os.path.join(conf_dir, 'lichess.conf'))
    except ParsingError as e:
        e.message = f'Error parsing configuration file {e.source}:\n{e.message}'
        raise CorruptedSourceError(e)

    return config

def parse_args():
    def set_subparser(parser, parser_dict):
        subparsers = parser.add_subparsers(**parser_dict['kwargs'])
        for subparser_dict in parser_dict['subparsers']:
            subparser = subparsers.add_parser(**subparser_dict['kwargs'], formatter_class=SubcommandFormatter)
            if subparser_dict['parser_type'] == 'subparser':
                set_subparser(subparser, subparser_dict['subparser'])
            elif subparser_dict['parser_type'] == 'argument':
                set_argument(subparser, subparser_dict['args'])
    
    def set_argument(parser, arguments):
        for argument_dict in arguments:
            parser.add_argument(*argument_dict['name'], **argument_dict['kwargs'])

    conf_dir = os.path.join(HOME, 'etc')
    if not os.path.exists(conf_dir):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {conf_dir} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    parser_file = os.path.join(conf_dir, 'parser.json')
    if not os.path.isfile(parser_file):
        raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {parser_file} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        parser_dict = load(open(parser_file), 'r')
    except JSONDecodeError as e:
        raise CorruptedSourceError(e)

    parser = ArgumentParser(**parser_dict['kwargs'], formatter_class=BaseFormatter)
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()

if __name__ == '__main__':
    try:
        config = parse_config()
        args = parse_args()
        command = args.command
        if command == 'help':
            subcommand = args.subcommand
            if subcommand is None:
                subprocess.call(['lichess', '--help'])
            else:
                subprocess.call(['lichess'] + subcommand + ['--help'])
        else:
            def find_package(command, directory=os.path.dirname(os.path.realpath(__file__))):
                for elem in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, elem)):
                        pkg = find_package(command, os.path.join(directory, elem))
                        if pkg is not None:
                            return pkg
                    elif elem.startswith(command) and elem.endswith('.py'):
                        return os.path.basename(directory)
                return None
            
            package = find_package(command)
            if package is None:
                raise CorruptedSourceError(FileNotFoundError(f'Module {command}.py not found!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
        
            module = import_module(f'.{command}', package=package)
            module.main(args, config)
    except LichessError:
        info = sys.exc_info()
        type = info[0].__name__
        message = info[1]
        print(__file__, type, message, sep=': ', file=sys.stderr)
        sys.exit(1)