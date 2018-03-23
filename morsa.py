#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from json import dump, load
from os.path import join
from os import listdir, makedirs
from subprocess import Popen, PIPE
from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory, FileHistory

PROJECT_OPTIONS = ['exit', 'help', 'use', 'createProject', 'openProject', 'showInfo', 'showModules']
PROJECT_PATH = 'Temporal project [/tmp/morsa/]'

def load_modules():
    load_modules = {}
    files = filter(lambda x: not x.startswith('__') and not x.endswith('pyc'), listdir('modules/'))
    modules = map(lambda x: x.replace('.py',''), files)
    for m in modules:
        try:
            x = __import__('modules.{0}'.format(m), fromlist=[m.title()])
            load_modules[m] = getattr(x, m.title())()
        except:
            print('[-] Error loading module {0}'.format(m))
    
    return load_modules

def update_toolbar(cli):
    return [(Token.Toolbar, PROJECT_PATH)]

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

def print_help():
    print("""[?] MORSA commands:
    \thelp          - Print help message
    \texit          - Close MORSA
    \tuse           - Change the context to another module [use <module name>]
    \topenProject   - Open an existing MORSA project [openProject <project path>]
    \tcreateProject - Create a new project [createProject <project name> <project path>]
    \tshowInfo      - Show information from the current project
    \tshowModules   - Show all available modules
    \tsetHistory    - Add history file [setHistory <history path>]
    \tsetName       - Change project name [setName <project name>]
    \tsetPrath      - Change project paht [setPath <project path>]
    """)

def create_project(name, path):    
    config = {
        'name': name,
        'project_path': path,
        'config_path': join(path, '{0}.config'.format(name)),
        'history_path': join(path, '{0}.history'.format(name)),
    }

    makedirs(path)
    with open(config['config_path'], 'w') as config_file:
        dump(config, config_file)

    global PROJECT_PATH
    PROJECT_PATH = "{0} [{1}]".format(name, path)   
    history = FileHistory(config['history_path']) 

    return (config, history)
    
def open_project(path):
    config_file = filter(lambda x: x.endswith('.config'), listdir(path))[0]
    config = load(join(path, config_file))

    global PROJECT_PATH
    PROJECT_PATH = "{0} [{1}]".format(config['name'], path)

def main():
    print_logo()

    modules = load_modules()
    
    #Temporal project variables
    history = InMemoryHistory()    
    suggest = AutoSuggestFromHistory()
    config = {}

    words = WordCompleter(PROJECT_OPTIONS, ignore_case=True, WORD=True)

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
            
            elif 'createProject' in user_input:
                config, history = create_project(*user_input.split(' '))

            elif 'openProject' in user_input:
                open_project(*user_input.split(' '))

            elif 'showInfo' in user_input: #TODO
                #Print project info
                print('[+] Modules jobs:')
                for m in modules:
                    modules[m].show_info()

            elif 'showModules' in user_input:
                print("[+] Available modules:")
                for m in modules:
                    print("\t{0}".format(m))

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