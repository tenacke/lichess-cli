from __future__ import annotations

import os
import sys

from json import loads, dump, load
from tempfile import NamedTemporaryFile
from subprocess import CalledProcessError, check_output, call
from typing import Dict, Set

from lichess.utils import convert_to_boolean, Singleton, IOHandler, ETC
from lichess import CLIError, LichessError
from lichess import BaseClient
from .config import Config

class Token(BaseClient):
    _instance: Token | None = None
    
    def init(self, user: str | None = None) -> None:
        self.io = IOHandler()
        client = BaseClient()
    
        self.set_credentials(*client.get_credentials())
        self.user = user
        
        gpg_enabled = convert_to_boolean(client.get_option('token', 'gpgenable'))
        self.handler = self.get_handler(gpg_enabled)

    def get_handler(self, gpg_enabled: bool) -> FileHandler:
        if gpg_enabled:
            return GPGHandler(self.user)
        else:
            return JSONHandler(self)

    def add(self, key: str, token: str, yes: bool = False) -> None:
        data = self.handler.read()
        if key in data:
            if not yes and self.io.input(f'Key {key} already exists\nDo you want to overwrite? [y/N] ').lower() != 'y':
                return
        data[key] = token
        self.handler.write(data)
        self.io.print(f'Key {key} added')

    def remove(self, key: str) -> None:
        data = self.handler.read()
        if key not in data:
            raise CLIError(KeyError(f'Key {key} not found'))
    
        del data[key]
        self.io.print(f'Key {key} deleted safely')
        self.handler.write(data)

    def get(self, key: str) -> str:
        data = self.handler.read()
        if key not in data:
            raise CLIError(KeyError(f'Key {key} not found'))
        return data[key]

    def list(self, keys: bool = False, tokens: bool = False) -> Dict | Set:
        data = self.handler.read()
        if (keys and tokens):
            return data
        elif keys:
            return data.keys()
        elif tokens:
            return data.values()
        else:
            return data

    def clear(self, yes: bool = False) -> None:
        if yes or self.client.input('Do you want to clear all tokens? [y/N] ').lower() == 'y':
            self.handler.write({})
            self.io.print('Tokens cleared')


class FileHandler(Singleton):
    def init(self) -> None:
        self.io = IOHandler()
        self.client = BaseClient()

    def get_file(self, gpg_enabled) -> str:
        prefix = self.client.get_option('token', 'prefix')
        if gpg_enabled:
            file_name = prefix + '.gpg'
        else:
            file_name = prefix + '.json'
        return os.path.join(ETC, file_name)

    def read(self) -> Dict:
        raise NotImplementedError('This method must be implemented in the subclass')
    
    def write(self, data: Dict) -> None:
        raise NotImplementedError('This method must be implemented in the subclass')


class GPGHandler(FileHandler):
    def init(self, user: str | None = None) -> None:
        super().init()
        program = self.client.get_option('token', 'gpgprogram')
        args = self.client.get_option('token', 'gpgargs').split()
        passphrase = self.client.get_option('user', 'passphrase')

        self.args = [program] + args
        if passphrase != '':
            self.args += ['--passphrase', passphrase]
        
        self.user = user or self.client.get_option('user', 'email')
        self.token_file = self.get_file(True)

    def read(self) -> Dict:
        args = self.args.copy()
        if self.user != '':
            args += ['--local-user', self.user]
        args += ['--decrypt', self.token_file]

        try:
            data = check_output(args)
            return loads(data)
        except CalledProcessError as e:
            raise CLIError(e)
        
    def write(self, data: Dict) -> None:
        args = self.args.copy()
        if self.user == '':
            self.user = self.io.input('You cannot use gpg encryption without configuring user.email. Please enter GPG user email: ')
            if self.io.input(f'Do you want to use this user email ({self.user}) as your default? [y/N] ').lower() == 'y':
                self.save_user()
        
        args += ['--recipient', self.user, '--encrypt', '--output', self.token_file]

        with NamedTemporaryFile('w+') as temp_file:
            dump(data, temp_file)
            temp_file.seek(0)

            args.append(temp_file.name)
            return_code = call(args)
            if return_code != 0:
                raise CLIError(CalledProcessError(return_code, args))


    def save_user(self) -> None:
        try:
            config = Config()
            config.set('user.email', self.user)
        except LichessError as e:
            self.io.print('Error saving user email')
        except Exception as e:
            self.io.print('Errores saving user email')
        else:
            self.io.print('User email saved successfully')


class JSONHandler(FileHandler):
    def init(self, client: BaseClient) -> None:
        super().init(client)
        self.token_file = self.get_file(False)

    def read(self) -> Dict:
        try:
            with open(self.token_file, 'r') as f:
                return load(f)
        except ValueError as e:
            raise CLIError(e)
        
    def write(self, data: Dict) -> None:
        try:
            with open(self.token_file, 'w') as f:
                dump(data, f)
        except ValueError as e:
            raise CLIError(e)
        