#!/usr/bin/env python3

import os
import sys
import json
import callect
import requests


url_releases = "https://api.github.com/repos/4surix/callect/releases"


def term_title(t):
    if os.name == "nt":
        # Windows
        os.system("title " + t)
    else:
        # Linux, Darwin (macOS, iOS, ...), *BSD
        print('\33]0;' + t + '\a', end='', flush=True)


args = sys.argv

term_title("Callect")

if len(args) == 1:
    # Si l'user a juste ouvert l'executable à la main
    # args[0] = Emplacement de l'executable


    derniere_version = ''

    response = requests.get(url_releases)

    if response.status_code == 200:
        infos = response.json()

        if infos[0]['tag_name'] != 'v' + callect.__version__:
            derniere_version = f"\nDernière version publique: {infos[0]['tag_name']}"


    print(
         f"Callect Langage - Version {callect.__version__}{derniere_version}"
        + "\n\nEcrivez ``` pour ouvrir et fermer un bloc de texte."
    )

    data = ""
    is_multiline = False

    while True:

        if is_multiline:
            try:
                text = input('... ')
            except KeyboardInterrupt:
                # CTRL + C
                data = ""
                text = ""
                is_multiline = False
                pass
            except EOFError:
                # CTRL + D
                data = ""
                text = ""
                is_multiline = False
                pass
        else:
            try:
                text = input('>>> ')
            except KeyboardInterrupt:
                # CTRL + C
                print("KeyboardInterrupt")
                sys.exit()
            except EOFError:
                # CTRL + D
                sys.exit()

        if text == '```':
            is_multiline = not is_multiline

        else:
            data += (text + '\n')

        if is_multiline:
            continue

        result = callect.run(data, args[0])
        if result:
            print('\n'.join(map(str, result)))

        data = ""

else:
    # Si l'user a ouvert l'executable avec un fichier

    path_exe = args[0]
    path_file = args[1]

    term_title("Callect - %s" % path_file)

    with open(path_file, encoding='utf-8-sig') as f:
        data = f.read()

    path_file = path_file.replace('\\', '/')
    path_exe = path_exe.replace('\\', '/')

    result = callect.run(data, path_file, path_exe)

    if result:
        print('\n'.join(map(str, result)))
