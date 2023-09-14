#!/usr/bin/env python3

from __future__ import annotations

import argparse
from argparse import _MutuallyExclusiveGroup, Action
from collections.abc import Iterable
import json
import configparser
import os
import importlib
import sys
import subprocess

from gettext import gettext as _

class BaseFormatter(argparse.HelpFormatter):
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


home = os.getenv('LICHESS_HOME')
if home is None:
    os.environ['LICHESS_HOME'] = os.path.expanduser('~/.lichess')
    home = os.getenv('LICHESS_HOME')


def parse_config():
    config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    config.read(os.path.join(home, 'defaults.conf'))
    config.read(os.path.join(home, 'lichess.conf'))
    # TODO handle corrupted config
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

    parser_dict = json.load(open(os.path.join(home, 'parser.json'), 'r'))
    # TODO handle corrupted config

    parser = argparse.ArgumentParser(**parser_dict['kwargs'], formatter_class=BaseFormatter)
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()

if __name__ == '__main__':
    config = parse_config()
    args = parse_args()
    command = args.command
    if command == 'help':
        subcommand = args.subcommand
        if subcommand is None:
            subprocess.call(['lichess', '--help'])
        else:
            subprocess.call(['lichess'] + subcommand + ['--help'])
        sys.exit(0)
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
        # TODO handle corrupted source
        module = importlib.import_module(f'.{command}', package=package)
        module.main(args, config)