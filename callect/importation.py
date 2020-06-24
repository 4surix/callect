
import os
import platform

name_system = platform.system()


from .types.table import mk_table
from .errors import ModuleNotFound, NotItem


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


class Module:

    def __init__(self, variables, chemin):
        self.call__ = lambda *args: self

        self.chemin = chemin
        self.variables = variables

    def __str__(self):
        return '<Module %s>' % self.chemin

    def __repr__(self):
        return '<Module %s>' % self.chemin

    def __call__(self, *args):
        return self


    def __bool__(self):
        return True

    def bool__(self, variables):
        return True__


    def __getitem__(self, item):
        try:
            value = self.variables.get(item)
        except:
            raise NotItem(self, item, item.ligne__)

        if value.__class__.__name__ == 'Objet':
            if not value.variables_modules:
                value.variables_modules = self.variables

        return value

    def __setitem__(self, item, value):
        self.variables.set(mk_txt(item), value)


    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value


def import_(decode):

    class Import:

        def call__(variables, args, kwargs):

            path_exe__ = variables.path_exe
            path_file__ = variables.path_file


            if path_exe__:
                path_exe = os.path.dirname(path_exe__)

            else:

                if name_system == 'Linux':
                    path_exe = '.'

                elif name_system == 'Windows':
                    path_exe = "C:/Users/%s/AppData/Roaming/Callect" % os.environ['USERNAME']

                elif name_system == 'Darwin':
                    path_exe = '.'


            if path_file__:
                path_file = os.path.dirname(path_file__)

            else:
                path_file = '.'


            data, path_file = get_data_module(args[0], path_file, path_exe)

            bloc = decode(data, path_file)

            variables = variables.__class__(
                [variables.variables[-1]],
                {}, 
                variables.events_date, 
                variables.events_keys, 
                path_file,
                path_exe__
            ).add({})

            bloc(variables)

            return Module(variables, path_file)

    return Import