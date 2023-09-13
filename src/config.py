import json
import os
import sys
import subprocess

settings = None

def check_valid_key(key):
    if '.' not in key:
        print('Invalid key\nYou should use the format section.option')
        subprocess.call(['lichess', 'config', 'get', '--help'])
        sys.exit(1)
    section, option = key.split('.')
    if not settings.has_section(section):
        print('Invalid section:', section)
        subprocess.call(['lichess', 'config', 'get', '--help'])
        sys.exit(1)
    if not settings.has_option(section, option):
        print('Invalid option:', option)
        subprocess.call(['lichess', 'config', 'get', '--help'])
        sys.exit(1)
    
    return section, option


def set_config(key, value, config):
    section, option = check_valid_key(key)


def get_config(key, config):
    section, option = check_valid_key(key)
    print(config.get(section, option))


def main(args, config):
    global settings

    home = os.getenv('LICHESS_HOME')
    config_file = os.path.join(home, 'lichess.conf')
    settings = config

    subcommand = args.subcommand
    if subcommand == 'set':
        set_config(args.key[0], args.value, config)
    elif subcommand == 'get':
        get_config(args.key[0], config)
    
