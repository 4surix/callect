import sys
import os
import callect


args = sys.argv

os.system("title Callect")


if len(args) == 1:
    # Si l'user a juste ouvert l'executable à la main
    # args[0] = Emplacement de l'executable

    print(
         f"Callect Langage - Version {callect.__version__}"
        + "\n\nEcrivez ``` pour ouvrir et fermer un bloc de texte."
    )

    data = ""
    in_plusiers_lignes = False

    while True:

        if in_plusiers_lignes:
            text = input('... ')
        else:
            text = input('>>> ')

        if text == '```':
            if in_plusiers_lignes:
                in_plusiers_lignes = False
            else:
                in_plusiers_lignes = True

        else:
            data += (text + '\n')

        if in_plusiers_lignes:
            continue

        result = callect.run(data, args[0])
        if result:
            print('\n'.join(map(str, result)))

        data = ""

else:
    # Si l'user a ouvert l'executable avec un fichier

    path_exe = args[0]
    path_file = args[1]

    os.system("title Callect - %s" % path_file)

    with open(path_file, encoding='utf-8') as f:
        data = f.read()

    path_file = '/'.join(path_file.split('\\'))
    result = callect.run(data, path_file, path_exe)

    if result:
        print('\n'.join(map(str, result)))