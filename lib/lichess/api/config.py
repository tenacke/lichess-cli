from __future__ import annotations

import json
import configparser
import os
import sys
import subprocess

settings = None

class Config:
    pass

def check_valid_key(key):
    if '.' not in key:
        print('Invalid key\nYou should use the format section.option')
        subprocess.call(['lichess', 'config', '--help'])
        sys.exit(1)
    section, option = key.split('.')
    if not settings.has_section(section):
        print('Invalid section:', section)
        subprocess.call(['lichess', 'config', '--help'])
        sys.exit(1)
    if not settings.has_option(section, option):
        print('Invalid option:', option)
        subprocess.call(['lichess', 'config', '--help'])
        sys.exit(1)
    
    return section, option


def set_config(key, value):
    section, option = check_valid_key(key)

    config_file = os.path.join(os.getenv('LICHESS_HOME'), 'lichess.conf')
    # TODO handle corrupted config
    config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    config.read(config_file)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, option, value)
    with open(config_file, 'w') as f:
        config.write(f)


def get_config(key):
    section, option = check_valid_key(key)
    print(settings.get(section, option))


def main(args, config):
    global settings
    settings = config

    subcommand = args.subcommand
    if subcommand == 'set':
        set_config(args.key[0], args.value)
    elif subcommand == 'get':
        get_config(args.key[0])
    
