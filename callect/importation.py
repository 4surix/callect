from .types.table import mk_table

from .errors import ModuleNotFound

import os

#Modules -------------------------------------------


chemin_modules = "C:/Users/%s/AppData/Roaming/Callect/modules" % os.environ['USERNAME']
#chemin_modules = os.path.dirname(os.path.dirname(__file__)) + "/modules"

#Création du dossier "modules" si n'existe pas
os.makedirs(chemin_modules, exist_ok=True)


def get_modules():
    return [m.split('.')[0] for m in os.listdir(chemin_modules)]

def get_data_module(module_txt, chemin=None):

    module = str(module_txt)

    if chemin:

        for partie in module.split('/'):
            if partie != '..':
                break
            _, module = module.split('/', 1)
            chemin = os.path.dirname(chemin)

        fichier = '%s/%s.cal' % (chemin, module)

        if not os.path.exists(fichier):
            fichier = '%s/%s.cal' % (chemin_modules, module)

    else:
        fichier = '%s/%s.cal' % (chemin_modules, module)

    try:
        with open(fichier, encoding='utf-8') as m:
            data = m.read()
        return data, fichier

    except FileNotFoundError:
        raise ModuleNotFound(module, module_txt.ligne__)

def import_(decode):

    class Import:

        def call__(variables, args, kwargs):

            path = os.path.dirname(variables.path)

            data, path = get_data_module(args[0], chemin=path)

            bloc = decode(data, path)

            vars__ = {}

            bloc(variables.add(vars__))

            variables.variables[0].update(vars__)

            return mk_table(_dict=vars__)

    return Import