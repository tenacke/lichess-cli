from __future__ import annotations

from argparse import Namespace
from configparser import RawConfigParser
from typing import Any, Dict, Iterator

from lichess import convert_to_boolean
from lichess import BaseClient
from .client import QueryClient

BASE_URL = None


class Account(BaseClient):
    pass

def info(api: QueryClient, ) -> Dict[str, Any] | Iterator[Any]:
    path = '/api/account'
    return api.get(path)


def email(api: QueryClient, ) -> str:
    path = '/api/account/email'
    return api.get(path)['email']


def preferences(api: QueryClient, ):
    path = '/api/account/preferences'
    return api.get(path)


def kid(api: QueryClient, value: bool = None):
    path = '/api/account/kid'
    if value is not None:
        params = {'v': convert_to_boolean(value)}
        return api.post(path, params=params)
    else:
        return api.get(path)['kid']


def bot(api: QueryClient, ):
    path = '/api/bot/account/upgrade'
    return api.post(path)


def main(args: Namespace, config: RawConfigParser):
    key = args.key[0] if args.key else None
    api = QueryClient(base_url=BASE_URL, token_key=key)
    
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