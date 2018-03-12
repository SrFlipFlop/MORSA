#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from os import listdir
from subprocess import Popen, PIPE
from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory, FileHistory

PROJECT_OPTIONS = ['exit', 'help', 'use', 'createProject', 'openProject', 'showInfo', 'setHistory', 'setName', 'setPath']

def print_logo():
    process = Popen(['stty', 'size'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    rows, columns = map(lambda x: int(x), stdout.split())

    if rows > 25 and columns > 92:
        print("""
         .-9 9 `\\
       =(:(::)=  ;
         ||||     \\                   /$$      /$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ 
         ||||      `-.                | $$$    /$$$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$
        ,\|\|         `,              | $$$$  /$$$$| $$  \ $$| $$  \ $$| $$  \__/| $$  \ $$
       /                \\             | $$ $$/$$ $$| $$  | $$| $$$$$$$/|  $$$$$$ | $$$$$$$$
      ;                  `'---.,      | $$  $$$| $$| $$  | $$| $$__  $$ \____  $$| $$__  $$
      |                         `\\    | $$\  $ | $$| $$  | $$| $$  \ $$ /$$  \ $$| $$  | $$
      ;                     /     |   | $$ \/  | $$|  $$$$$$/| $$  | $$|  $$$$$$/| $$  | $$
      \                    |      /   |__/     |__/ \______/ |__/  |__/ \______/ |__/  |__/
       )           \  __,.--\    /
    .-' \,..._\     \`   .-'  .-'
   `-=``      `:    |   /-/-/`
                `.__/
        """)  
    
    elif rows > 24 and columns > 44:
        print("""
          .-9 9 `\\
       =(:(::)=  ;
         ||||     \\
         ||||      `-.
        ,\|\|         `,
       /                \\
      ;                  `'---., 
      |                         `\\
      ;                     /     |
      \                    |      /
       )           \  __,.--\    /
    .-' \,..._\     \`   .-'  .-'
   `-=``      `:    |   /-/-/`
                `.__/       
        """)
    
    elif rows > 21 and columns > 58:
        print("""
     /$$      /$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$
    | $$$    /$$$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$
    | $$$$  /$$$$| $$  \ $$| $$  \ $$| $$  \__/| $$  \ $$
    | $$ $$/$$ $$| $$  | $$| $$$$$$$/|  $$$$$$ | $$$$$$$$
    | $$  $$$| $$| $$  | $$| $$__  $$ \____  $$| $$__  $$
    | $$\  $ | $$| $$  | $$| $$  \ $$ /$$  \ $$| $$  | $$
    | $$ \/  | $$|  $$$$$$/| $$  | $$|  $$$$$$/| $$  | $$
    |__/     |__/ \______/ |__/  |__/ \______/ |__/  |__/
        """)

    else:
        print("Welcome to MORSA!")

def load_modules():
    load_modules = {}
    files = filter(lambda x: not x.startswith('__') and not x.endswith('pyc'), listdir('modules/'))
    modules = map(lambda x: x.replace('.py',''), files)
    for m in modules:
        x = __import__('modules.{0}'.format(m), fromlist=[m.title()])
        load_modules[m] = getattr(x, m.title())()
    
    return load_modules

def print_help():
    print('TODO!')

def update_toolbar(cli, title='Temporal project [/tmp/morsa/]'):
    return [(Token.Toolbar, title)]

def main():
    print_logo()

    modules = load_modules()
    
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

        if not module: #Base        
            if user_input == 'help':
                print_help()

            elif user_input == 'exit':
                end = True           

            elif 'use' in user_input:
                module = user_input.split(' ')[1]
                if not module in modules:
                    module = None
                    print('[-] Module "{0}" not found.'.format(module))
                else:
                    words = WordCompleter(modules[module].words, ignore_case=True)
            
            elif 'createProject' in user_input: #TODO
                pass

            elif 'openProject' in user_input: #TODO
                pass

            elif 'showInfo' in user_input: #TODO
                pass

            elif 'setHistory' in user_input:
                path = user_input.split(' ')[2]
                history = FileHistory(path)
                print('[+] New history file: {0}'.format(path))

            elif 'setName' in user_input: #TODO
                pass

            elif 'setPath' in user_input: #TODO
                pass

            else:
                print('[-] Option "{0}" not found. Please use "help" to see the correct options.'.format(user_input))

        else:
            if user_input == 'back':
                module = None
                words = WordCompleter(PROJECT_OPTIONS, ignore_case=True)
            
            else:
                modules[module].run(user_input)

if __name__ == '__main__':
    main()