from __future__ import annotations

import json
import os
import sys
import tempfile
import subprocess

from typing import Dict, Set
from configparser import RawConfigParser
from argparse import Namespace

from utils.exceptions import CLIError

_settings = None
_VERBOSE = None

def print_verbose(*args):
    if _VERBOSE:
        print(*args)


def read_json() -> Dict:
    if _settings is None:
        raise CLIError('Settings not configured')

    gpg_enabled = _settings.getboolean('token', 'gpgenable')
    gpg_program = _settings.get('token', 'gpgprogram')
    gpg_args = _settings.get('token', 'gpgargs').split()
    gpg_passphrase = _settings.get('user', 'passphrase')
    gpg_user = _settings.get('user', 'email')
    
    token_file = _settings.get('runtime', 'token_file')

    if gpg_enabled:   
        args = [gpg_program] + gpg_args 
        if gpg_passphrase != '':
            args += ['--passphrase', gpg_passphrase]
        if gpg_user != '':
            args += ['--local-user', gpg_user]
        args += ['--decrypt', token_file]
        
        try:
            data = subprocess.check_output(args)
            return json.loads(data)
        except subprocess.CalledProcessError:
            raise CLIError('Error reading token file')
    else:
        try:
            with open(token_file, 'r') as f:
                return json.load(f)
        except IOError:
            raise CLIError('Error reading token file')


def write_json(data: Dict) -> None:
    if _settings is None:
        raise CLIError('Settings not configured')

    gpg_enabled = _settings.getboolean('token', 'gpgenable')
    gpg_program = _settings.get('token', 'gpgprogram')
    gpg_args = _settings.get('token', 'gpgargs').split()
    gpg_passphrase = _settings.get('user', 'passphrase')
    gpg_user = _settings.get('user', 'email')
    
    token_file = _settings.get('runtime', 'token_file')

    if gpg_enabled:
        with tempfile.NamedTemporaryFile('w+') as temp_file:
            json.dump(data, temp_file)
            temp_file.seek(0)

            args = [gpg_program] + gpg_args
            save_default = False
            if gpg_passphrase != '':
                args += ['--passphrase', gpg_passphrase]
            if gpg_user == '':
                gpg_user = input('You cannot use gpg encryption without configuring user.name. Please enter GPG user email: ')
                save_default = input('Do you want to use this user email as your default? [y/N] ').lower() == 'y'
            args += ['--recipient', gpg_user, '--encrypt', '--output', token_file, temp_file.name]

            return_code = subprocess.call(args)
            if return_code != 0:
                raise CLIError('Error writing token file')

            if save_default:
                subprocess.call(['lichess', 'config', 'set', 'user.email', gpg_user])
    else:
        try:
            with open(token_file, 'w') as f:
                json.dump(data, f)
        except IOError:
            raise CLIError('Error writing token file')


def add_token(key: str, token: str, yes: bool = False) -> None:
    data = read_json()
    if key in data:
        if not yes and input(f'Key {key} already exists\nDo you want to overwrite? [y/N] ').lower() != 'y':
            return
    data[key] = token
    write_json(data)
    print_verbose(f'Key {key} added')


def get_token(key: str) -> str:
    data = read_json()
    if key not in data:
        raise CLIError(f'Key {key} not found')
    return data[key]


def remove_token(key: str) -> None:
    data = read_json()
    if key not in data:
        raise CLIError(f'Key {key} not found')
    
    del data[key]
    print_verbose(f'Key {key} deleted safely')
    write_json(data)


def list_tokens(keys: bool = False, tokens: bool = False) -> Dict | Set:
    data = read_json()
    if (keys and tokens):
        return data
    elif keys:
        return data.keys()
    elif tokens:
        return data.values()
    else:
        return data


def clear_tokens(yes: bool = False) -> None:
    if not yes and input('Do you want to clear all tokens? [y/N] ').lower() != 'y':
        return
    write_json({})
    print_verbose('Tokens cleared')


def configure(config: RawConfigParser, verbose: bool = True) -> None:
    global _settings
    global _VERBOSE

    _VERBOSE = verbose

    _settings = config
    _settings.add_section('runtime')
    
    home = os.getenv('LICHESS_HOME')
    token_prefix = config.get('token', 'prefix')
    gpg_enabled = _settings.getboolean('token', 'gpgenable')
    
    if gpg_enabled:
        _settings.set('runtime', 'token_file', os.path.join(home, token_prefix + '.gpg'))
    else:
        _settings.set('runtime', 'token_file', os.path.join(home, token_prefix + '.json'))


def main(args: Namespace, config: RawConfigParser) -> None:
    configure(config)

    subcommand = args.subcommand
    if subcommand == 'add':
        add_token(args.key[0], args.token[0], yes=args.yes)
    elif subcommand == 'get':
        print(get_token(args.key[0]))
    elif subcommand == 'remove':
        remove_token(args.key[0])
    elif subcommand == 'list':
        data = list_tokens(args.keys, args.tokens)
        print('\n'.join([f'{key}: {value}' for key, value in data.items()] if isinstance(data, dict) else data))
    elif subcommand == 'clear':
        clear_tokens(args.yes)