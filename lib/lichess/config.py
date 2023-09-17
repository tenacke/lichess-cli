from __future__ import annotations

import os
from configparser import RawConfigParser, ConfigParser, ParsingError
from typing import Dict, Any

from .base import BaseClient
from .utils import IOHandler, ETC
from .exceptions import CorruptedSourceError, UserError


CONFIG_FILE = os.path.join(ETC, 'lichess.conf')
DEFAULTS_FILE = os.path.join(ETC, 'defaults.conf')

def parse_config(include_defaults: bool = True) -> RawConfigParser:
    config = ConfigParser(inline_comment_prefixes=('#', ';'))
    
    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        if include_defaults:
            if os.path.isfile(DEFAULTS_FILE):
                config.read(DEFAULTS_FILE)
            else:
                raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {DEFAULTS_FILE} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
        
        if os.path.isfile(CONFIG_FILE):
            config.read(CONFIG_FILE)
    except ParsingError as e:
        e.message = f'Error parsing configuration file {e.source}:\n{e.message}'
        raise CorruptedSourceError(e)

    return config


class Config(BaseClient):
    _instance: Config | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        self.config = parse_config(include_defaults=True)
        self.temp_config = parse_config(include_defaults=False)
    
    def new(self, verbose: bool = True) -> None:
        self.io = IOHandler(verbose)

    def has_section(self, section: str) -> bool:
        return self.config.has_section(section)
    
    def has_option(self, section: str, option: str) -> bool:
        if not self.config.has_section(section):
            return False
        return self.config.has_option(section, option)
    
    def add_section(self, section: str) -> None:
        self.config.add_section(section)

    def set_option(self, section: str, option: str, value: str) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_section(self, section: str) -> Dict[str, str]:
        if not self.config.has_section(section):
            raise KeyError(f'Section {section} not found')
        return dict(self.config.items(section))

    def get_option(self, section: str, option: str) -> str:
        if not self.config.has_option(section, option):
            raise KeyError(f'Option {option} not found in section {section}')
        return self.config.get(section, option)
    
    def get(self, key: str) -> str:
        key = key[0]
        section, option = self.check_valid_key(key)
        self.io.print(f'{key}: {self.get_option(section, option)}')
    
    def set(self, key: str, value: str) -> None:
        key = key[0]

        section, option = self.check_valid_key(key)
        if self.has_option(section, option):
            temp = self.get_option(section, option)
        self.set_option(section, option, value)

        if not self.temp_config.has_section(section):
            self.temp_config.add_section(section)
        self.temp_config.set(section, option, value)

        try:
            with open(CONFIG_FILE, 'w') as f:
                self.temp_config.write(f)
            self.io.print(f'Setting {key} successfully set to {value}')
        except OSError as e:
            self.set_option(section, option, temp)
            self.io.print(f'Error setting {key}')
            raise UserError(e)

    def check_valid_key(self, key):
        if key.count('.') != 1:
            raise UserError(ValueError('Invalid format. You should use the format section.option'))
            
        section, option = key.split('.')
        if not self.config.has_section(section):
            raise UserError(KeyError(f'Section {section} not found'))
        
        if not self.config.has_option(section, option):
            raise UserError(KeyError(f'Option {option} not found in section {section}'))
        
        return section, option
