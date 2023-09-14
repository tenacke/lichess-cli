from __future__ import annotations

from argparse import Namespace
from configparser import RawConfigParser
from typing import Any, Dict, Iterator

from api import APIClient
from utils import convert_to_boolean

BASE_URL = None

def info(api: APIClient, ) -> Dict[str, Any] | Iterator[Any]:
    path = '/api/account'
    return api.get(path)


def email(api: APIClient, ) -> str:
    path = '/api/account/email'
    return api.get(path)['email']


def preferences(api: APIClient, ):
    path = '/api/account/preferences'
    return api.get(path)


def kid(api: APIClient, value: bool = None):
    path = '/api/account/kid'
    if value is not None:
        params = {'v': convert_to_boolean(value)}
        return api.post(path, params=params)
    else:
        return api.get(path)['kid']


def bot(api: APIClient, ):
    path = '/api/bot/account/upgrade'
    return api.post(path)


def main(args: Namespace, config: RawConfigParser):
    key = args.key[0] if args.key else None
    api = APIClient(config, base_url=BASE_URL, token_key=key)
    
    subcommand = args.subcommand
    if subcommand == 'info':
        print(info(api))
    elif subcommand == 'email':
        print(email(api))
    elif subcommand == 'preferences':
        print(preferences(api))
    elif subcommand == 'kid':
        print(kid(api, args.mode))
    elif subcommand == 'bot':
        print(bot(api))