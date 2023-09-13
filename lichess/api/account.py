import berserk
import os
import sys
import subprocess 




def main(args, config):
    token_key = config.get('token', 'key')
    token = subprocess.check_output(['lichess', 'token', 'get', token_key]).decode('utf-8').strip()
    print(token)