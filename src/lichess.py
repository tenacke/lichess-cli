#!/usr/bin/env python3

import argparse
import json
import configparser
import os
import importlib

home = os.getenv('LICHESS_HOME')
if home is None:
    os.environ['LICHESS_HOME'] = os.path.expanduser('~/.lichess')
    home = os.getenv('LICHESS_HOME')


def parse_config():
    config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    config.read(os.path.join(home, 'defaults.conf'))
    config.read(os.path.join(home, 'lichess.conf'))
    return config

def parse_args():
    def set_subparser(parser, parser_dict):
        subparsers = parser.add_subparsers(**parser_dict['kwargs'])
        for subparser_dict in parser_dict['subparsers']:
            subparser = subparsers.add_parser(**subparser_dict['kwargs'])
            if subparser_dict['parser_type'] == 'subparser':
                set_subparser(subparser, subparser_dict['subparser'])
            elif subparser_dict['parser_type'] == 'argument':
                set_argument(subparser, subparser_dict['args'])
    
    def set_argument(parser, arguments):
        for argument_dict in arguments:
            parser.add_argument(*argument_dict['name'], **argument_dict['kwargs'])

    parser_dict = json.load(open(os.path.join(home, 'parser.json'), 'r'))

    parser = argparse.ArgumentParser(**parser_dict['kwargs'])
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()

if __name__ == '__main__':
    config = parse_config()
    args = parse_args()
    command = args.command
    module = importlib.import_module(command)
    module.main(args, config)
