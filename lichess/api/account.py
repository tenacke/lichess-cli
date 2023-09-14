import berserk
import os
import sys
import subprocess 


def info():
    pass


def email():
    pass


def preferences():
    pass


def kid():
    pass


def bot():
    pass

def main(args, config):
    token_key = config.get('token', 'key')
    token = subprocess.check_output(['lichess', 'token', 'get', token_key]).decode('utf-8').strip()
    print(token)