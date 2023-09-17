from __future__ import annotations

import os
import json
import subprocess

from tempfile import NamedTemporaryFile
from subprocess import CalledProcessError
from typing import Any, Dict, Set

from .utils import convert_to_boolean, Singleton, IOHandler, ETC
from .exceptions import CLIError, LichessError, UserError
from .base import BaseClient
from .config import Config

class Token(BaseClient):
    _instance: Token | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        config = Config(verbose=False)
        
        gpg_enabled = convert_to_boolean(config.get_option('token', 'gpgenable'))
        self.handler = self.get_handler(gpg_enabled)

        self.data = self.handler.read()

    def new(self, verbose: bool = True) -> None:
        self.io = IOHandler(verbose)

    def get_handler(self, gpg_enabled: bool) -> FileHandler:
        if gpg_enabled:
            return GPGHandler()
        else:
            return JSONHandler()

    def add(self, key: str, token: str, yes: bool = False) -> None:
        if key in self.data:
            if not yes and self.io.input(f'Key {key} already exists\nDo you want to overwrite? [y/N] ').lower() != 'y':
                return
        self.data[key] = token
        self.handler.write(self.data)
        self.io.print(f'Key {key} added')

    def remove(self, key: str) -> None:
        if key not in self.data:
            raise UserError(KeyError(f'Key {key} not found'))
    
        del self.data[key]
        self.io.print(f'Key {key} deleted safely')
        self.handler.write(self.data)

    def get(self, key: str) -> str:
        if key not in self.data:
            raise UserError(KeyError(f'Key {key} not found'))
        return self.data[key]

    def list(self, keys: bool = False, tokens: bool = False) -> Dict | Set:
        if (keys and tokens):
            return self.data
        elif keys:
            return self.data.keys()
        elif tokens:
            return self.data.values()
        else:
            return self.data

    def clear(self, yes: bool = False) -> None:
        if yes or self.io.input('Do you want to clear all tokens? [y/N] ').lower() == 'y':
            self.handler.write({})
            self.io.print('Tokens cleared')


class FileHandler(Singleton):
    def init(self) -> None:
        self.io = IOHandler()
        self.config = Config(verbose=False)

    def get_file(self, gpg_enabled: bool) -> str:
        prefix = self.config.get_option('token', 'prefix')
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
    def init(self) -> None:
        super().init()
        program = self.config.get_option('token', 'gpgprogram')
        args = self.config.get_option('token', 'gpgargs').split()
        passphrase = self.config.get_option('user', 'passphrase')

        self.args = [program] + args
        if passphrase != '':
            self.args += ['--passphrase', passphrase]
        
        self.user = self.config.get_option('user', 'email')
        self.token_file = self.get_file(True)

    def read(self) -> Dict:
        args = self.args.copy()
        if self.user != '':
            args += ['--local-user', self.user]
        args += ['--decrypt', self.token_file]

        try:
            data = subprocess.check_output(args)
            return json.loads(data)
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
            json.dump(data, temp_file)
            temp_file.seek(0)

            args.append(temp_file.name)
            return_code = subprocess.call(args)
            if return_code != 0:
                raise CLIError(CalledProcessError(return_code, args))


    def save_user(self) -> None:
        try:
            self.config.set('user.email', self.user)
        except LichessError as e:
            self.io.print('Error saving user email')
        else:
            self.io.print('User email saved successfully')


class JSONHandler(FileHandler):
    def init(self) -> None:
        super().init()
        self.token_file = self.get_file(False)

    def read(self) -> Dict:
        try:
            with open(self.token_file, 'r') as f:
                return json.load(f)
        except ValueError as e:
            raise CLIError(e)
        
    def write(self, data: Dict) -> None:
        try:
            with open(self.token_file, 'w') as f:
                json.dump(data, f)
        except ValueError as e:
            raise CLIError(e)
        