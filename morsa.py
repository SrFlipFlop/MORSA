#!/usr/bin/env python
from __future__ import print_function, unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory, FileHistory

def print_logo():
    print("""
            .-9 9 `\\
          =(:(::)=  ;
            ||||     \\                         /$$      /$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ 
            ||||      `-.                      | $$$    /$$$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$
           ,\|\|         `,                    | $$$$  /$$$$| $$  \ $$| $$  \ $$| $$  \__/| $$  \ $$
          /                \\                   | $$ $$/$$ $$| $$  | $$| $$$$$$$/|  $$$$$$ | $$$$$$$$
         ;                  `'---.,            | $$  $$$| $$| $$  | $$| $$__  $$ \____  $$| $$__  $$
         |                         `\\          | $$\  $ | $$| $$  | $$| $$  \ $$ /$$  \ $$| $$  | $$
         ;                     /     |         | $$ \/  | $$|  $$$$$$/| $$  | $$|  $$$$$$/| $$  | $$
         \                    |      /         |__/     |__/ \______/ |__/  |__/ \______/ |__/  |__/
          )           \  __,.--\    /
       .-' \,..._\     \`   .-'  .-'
      `-=``      `:    |   /-/-/`
                   `.__/
    """)

def update_toolbar(cli): #TODO: dynamic toolbar
    return [(Token.Toolbar, 'Toolbar text1')]

def main():
    #TODO: change logo for screen h/w
    #print_logo()

    #history = InMemoryHistory()
    history=FileHistory('/tmp/morsa_history.txt')
    suggest=AutoSuggestFromHistory()
    words = WordCompleter(['<html>', '<body>', '<head>', '<title>'], ignore_case=True)

    end = False
    while not end:
        user_input = prompt('> ', 
            completer=words, 
            history=history, 
            auto_suggest=suggest, 
            get_bottom_toolbar_tokens=update_toolbar)
        
        if user_input in ('exit', 'quit'):
            end = True
        else:
            print('[+] Nope: {0}'.format(user_input))

if __name__ == '__main__':
    main()