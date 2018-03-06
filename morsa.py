#!/usr/bin/env python
from __future__ import print_function, unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory, FileHistory

PROJECT_OPTIONS = ['exit', 'help', 'use', 'create', 'open', 'info', 'sethistory', 'setname', 'setpath']

def print_help():
    print('TODO!')

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

def update_toolbar(cli, title='Temporal project [/tmp/morsa/]'):
    return [(Token.Toolbar, title)]

def main():
    #TODO: print the logo depending on screen resolution

    #TODO: load all modules
    
    #Temporal project variables
    history = InMemoryHistory()    
    suggest = AutoSuggestFromHistory()    

    words = WordCompleter(PROJECT_OPTIONS, ignore_case=True)

    module = None
    end = False
    while not end:
        user_input = prompt(
            '({0})> '.format(module) if module else '> ',
            get_bottom_toolbar_tokens=update_toolbar,
            auto_suggest=suggest,
            completer=words,
            history=history
        )
        
        if user_input == 'help':
            print_help()

        elif user_input == 'exit':
            end = True
        
        elif 'sethistory' in user_input:
            path = user_input.split(' ')[2]
            print('[+] New history file: {0}'.format(path))
            history = FileHistory(path)

        elif 'use' in user_input:
            module = user_input.split(' ')[1]
            #TODO: send input to the module
        
        else:
            print('[-] Option "{0}" not found. Please use "help" to see the correct options.'.format(user_input))

if __name__ == '__main__':
    main()