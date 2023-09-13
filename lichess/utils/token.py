import json
import os
import sys
import tempfile
import subprocess

_settings = None
_VERBOSE = None

def print_verbose(*args):
    if _VERBOSE:
        print(*args)


def read_json():
    if _settings is None:
        print_verbose('Settings not configured')
        sys.exit(1)

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
            print_verbose('Error reading token file')
            sys.exit(1)
    else:
        try:
            with open(token_file, 'r') as f:
                return json.load(f)
        except IOError:
            print_verbose('Error reading token file')
            sys.exit(1)


def write_json(data):
    if _settings is None:
        print_verbose('Settings not configured')
        sys.exit(1)

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
                print_verbose('Error writing token file')
                sys.exit(1)

            if save_default:
                subprocess.call(['lichess', 'config', 'set', 'user.email', gpg_user])
    else:
        try:
            with open(token_file, 'w') as f:
                json.dump(data, f)
        except IOError:
            print_verbose('Error writing token file')
            sys.exit(1)


def add_token(key, token, yes=False):
    data = read_json()
    if key in data:
        if not yes and input(f'Key {key} already exists\nDo you want to overwrite? [y/N] ').lower() != 'y':
            sys.exit(1)
    data[key] = token
    write_json(data)
    print_verbose(f'Key {key} added')


def get_token(key):
    data = read_json()
    if key not in data:
        print_verbose(f'Key {key} not found')
        sys.exit(1)
    return data[key]


def remove_token(key):
    data = read_json()
    if key not in data:
        print_verbose(f'Key {key} not found')
        sys.exit(1)
    del data[key]
    print_verbose(f'Key {key} deleted safely')
    write_json(data)


def list_tokens(keys=False, tokens=False):
    data = read_json()
    if (keys and tokens):
        return data
    elif keys:
        return data.keys()
    elif tokens:
        return data.values()
    else:
        return data


def clear_tokens(yes=False):
    if not yes and input('Do you want to clear all tokens? [y/N] ').lower() != 'y':
        sys.exit(1)
    write_json({})
    print_verbose('Tokens cleared')


def configure(config, verbose=True):
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


def main(args, config):
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