
import os
import platform

name_system = platform.system()


from .types.table import mk_table
from .errors import ModuleNotFound


def get_data_module(module_txt, path_file, path_exe):

    module = str(module_txt)

    path_exe += '/modules'

    if path_file:

        for partie in module.split('/'):
            if partie != '..':
                break
            _, module = module.split('/', 1)
            path_file = os.path.dirname(path_file)

        fichier = '%s/%s.cal' % (path_file, module)

        if not os.path.exists(fichier):
            fichier = '%s/%s.cal' % (path_exe, module)

    else:
        fichier = '%s/%s.cal' % (path_exe, module)

    try:
        with open(fichier, encoding='utf-8') as m:
            data = m.read()
        return data, fichier

    except FileNotFoundError:
        raise ModuleNotFound(module, module_txt.ligne__)

def import_(decode):

    class Import:

        def call__(variables, args, kwargs):

            path_exe = variables.path_exe
            path_file = variables.path_file


            if path_exe:
                path_exe = os.path.dirname(path_exe)

            else:

                if name_system == 'Linux':
                    path_exe = '.'

                elif name_system == 'Windows':
                    path_exe = "C:/Users/%s/AppData/Roaming/Callect" % os.environ['USERNAME']

                elif name_system == 'Darwin':
                    path_exe = '.'


            if path_file:
                path_file = os.path.dirname(path_file)


            data, path = get_data_module(args[0], path_file, path_exe)

            bloc = decode(data, path)

            vars__ = {}

            bloc(variables.add(vars__))

            variables.variables[0].update(vars__)

            return mk_table(_dict=vars__)

    return Import