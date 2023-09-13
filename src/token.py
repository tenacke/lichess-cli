import json
import os
import sys
import tempfile
import subprocess

settings = dict()


def read_json():
    gpg_enabled = settings.get('gpg_enabled')
    gpg_program = settings.get('gpg_program')
    gpg_args = settings.get('gpg_args')
    gpg_passphrase = settings.get('gpg_passphrase', '')
    gpg_user = settings.get('gpg_user')
    token_file = settings.get('token_file')
    temp_token_file = settings.get('temp_token_file', None)

    if gpg_enabled:
        temp_token_file.seek(0)
        args = [gpg_program] + gpg_args 
        if gpg_passphrase != '':
            args += ['--passphrase', gpg_passphrase]
        if gpg_user != '':
            args += ['--local-user', gpg_user]
        args += ['--decrypt', token_file]
        return_code = subprocess.call(args, stdout=temp_token_file)
        if return_code != 0:
            print('Error reading token file')
            sys.exit(1)
        temp_token_file.seek(0)
        return json.load(temp_token_file)
    else:
        with open(token_file, 'r') as f:
            return json.load(f)
        

def write_json(data):
    gpg_enabled = settings.get('gpg_enabled')
    gpg_program = settings.get('gpg_program')
    gpg_args = settings.get('gpg_args')
    gpg_passphrase = settings.get('gpg_passphrase')
    gpg_user = settings.get('gpg_user')
    token_file = settings.get('token_file')
    temp_token_file = settings.get('temp_token_file')

    if gpg_enabled:
        temp_token_file.seek(0)
        json.dump(data, temp_token_file)
        temp_token_file.truncate()
        args = [gpg_program] + gpg_args
        save_default = False
        if gpg_passphrase != '':
            args += ['--passphrase', gpg_passphrase]
        if gpg_user != '':
            gpg_user = input('You cannot use gpg encryption without configuring user.name. Please enter GPG user email: ')
            save_default = input('Do you want to use this user email as your default? [y/N] ').lower() == 'y'
        args += ['--recipient', gpg_user, '--encrypt', '--output', token_file, temp_token_file.name]

        return_code = subprocess.call(args)
        if return_code != 0:
            print('Error writing token file')
            sys.exit(1)

        if save_default:
            subprocess.call(['lichess', 'config', 'set', 'user.email', gpg_user])
    else:
        with open(token_file, 'w') as f:
            json.dump(data, f)


def add_token(key, token, yes=False):
    data = read_json()
    if key in data:
        if not yes and input(f'Key {key} already exists\nDo you want to overwrite? [y/N] ').lower() != 'y':
            sys.exit(1)
    data[key] = token
    write_json(data)
    print(f'Key {key} added')


def get_token(key):
    data = read_json()
    if key not in data:
        print(f'Key {key} not found')
        sys.exit(1)
    print(data[key])


def remove_token(key):
    data = read_json()
    if key not in data:
        print(f'Key {key} not found')
        sys.exit(1)
    del data[key]
    write_json(data)


def list_tokens(keys=False, tokens=False):
    data = read_json()
    if (keys and tokens):
        print('\n'.join([f'{key}: {value}' for key, value in data.items()]))
    elif keys:
        print('\n'.join(data.keys()))
    elif tokens:
        print('\n'.join(data.values()))
    else:
        print('\n'.join([f'{key}: {value}' for key, value in data.items()]))


def clear_tokens(yes=False):
    if not yes and input('Do you want to clear all tokens? [y/N] ').lower() != 'y':
        sys.exit(1)
    write_json({})
    print('Tokens cleared')


def main(args, config):
    global settings

    home = os.getenv('LICHESS_HOME')
    token_prefix = config.get('token', 'prefix')
    settings['gpg_enabled'] = config.getboolean('token', 'gpgenable')
    settings['gpg_program'] = config.get('token', 'gpgprogram')
    settings['gpg_args'] = config.get('token', 'gpgargs').split()
    settings['gpg_passphrase'] = config.get('user', 'passphrase')
    settings['gpg_user'] = config.get('user', 'email')
    
    if settings['gpg_enabled']:
        settings['token_file'] = os.path.join(home, token_prefix + '.gpg')
        settings['temp_token_file'] = tempfile.NamedTemporaryFile(mode='w+')
    else:
        settings['token_file'] = os.path.join(home, token_prefix + '.json')

    subcommand = args.subcommand
    if subcommand == 'add':
        add_token(args.key[0], args.token[0], yes=args.yes)
    elif subcommand == 'get':
        get_token(args.key[0])
    elif subcommand == 'remove':
        remove_token(args.key[0])
    elif subcommand == 'list':
        list_tokens(args.keys, args.tokens)
    elif subcommand == 'clear':
        clear_tokens(args.yes)