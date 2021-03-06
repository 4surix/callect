
__version__ = "1.0.0-pre6"


import traceback
import sys


from . import events
from . import types
from .errors import NotDefined, ALLExcept
from .decode import decode
from .built_in import fonctions_intégrées


fonctions_intégrées['version__'] = types.txt.mk_txt(__version__)


def run(data, path_file, path_exe=None):

    try:
        data = decode(data, path_file)

        try:
            variables = Info(
                [fonctions_intégrées], {}, [], [], path_file, path_exe
            ).add({})

            threads = events.run(variables)
        
            value = data(variables)

            for thread in threads:
                # On termine le thread
                thread.running = False

            return value

        except ALLExcept as e:
            msg_exception = (
                f"Exception run:\n\n{e}\n\n\nPress Entrée to exit.\n"
            )

        except Exception as e:
            msg_exception = (
                'Exception run Python:\n\n'
                + traceback.format_exc()
                + "\n\n\nPress Entrée to exit.\n"
            )

    except ALLExcept as e:
        msg_exception = (
            f"Exception decode:\n\n{e}\n\n\nPress Entrée to exit.\n"
        )

    except Exception as e:
        msg_exception = (
            'Exception decode Python:\n\n' 
            + traceback.format_exc() 
            + "\n\n\nPress Entrée to exit.\n"
        )

    try: input(msg_exception)
    except KeyboardInterrupt:
        # CTRL + C
        print("KeyboardInterrupt")
        sys.exit()
    except EOFError:
        # CTRL + D
        sys.exit()


class Info:

    def __init__(self, 
        variables=None, 
        events_vars=None,
        events_date=None,
        events_keys=None,
        path_file=None, 
        path_exe=None
    ):

        self.variables = variables if variables else [{}]

        self.events_vars = events_vars if events_vars else {}
        self.events_date = events_date if events_date else []
        self.events_keys = events_keys if events_keys else []

        self.path_exe = path_exe
        self.path_file = path_file

        self.get_event = self.events_vars.get

        self.action_ligne__ = ''

    def add(self, variables, events_vars={}):
        return Info(
            [variables] + self.variables, 
            self.events_vars.copy().update(events_vars),
            self.events_date,
            self.events_keys,
            self.path_file, 
            self.path_exe
        )

    def get(self, var, ligne=None, is_global=False, is_local=False):

        if is_global:
            variables = self.variables[1:]

        elif is_local:
            variables = self.variables[:1]

        else:
            variables = self.variables

        for variables in variables:
            value = variables.get(var)
            if value is not None:
                return value

        raise NotDefined(var, ligne if ligne else '')

    def set(self, var, value, is_global=False):

        if is_global:
            for variables in self.variables[1:-1]:
                if var in variables:
                    variables[var] = value
                    return

        self.variables[0][var] = value

    def set_event(self, event):

        event.variables = self

        if event.type == 'changevars':

            for var in event.vars:
                if var not in self.events_vars:
                    self.events_vars[var] = [event]
                else:
                    self.events_vars[var].append(event)

        elif event.type == 'changedate':

            self.events_date.append(event)

        elif event.type == 'keypress':

            self.events_keys.append(event)