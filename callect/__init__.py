
__version__ = "1.0.0-pre1"


from .errors import NotDefined, ALLExcept

from .decode import decode

from .built_in import fonctions_intégrées

import traceback

import time

import sys


def calcul_time(func):
    
    temps = []

    for _ in range(30):
        start_time = time.time()

        func()

        temps.append(time.time() - start_time)

    value = 0
    for t in temps:
        value += t

    return value/len(temps)


def run(data, path_file, path_exe=None, *, time=False):

    msg_exception = None

    try:
        data = decode(data, path_file)

        try:

            if time:
                print(calcul_time(lambda: data(Info([fonctions_intégrées], {}, path_file, path_exe).add({}))))

            else:
                data(Info([fonctions_intégrées], {}, path_file, path_exe).add({}))

        except ALLExcept as e:
            msg_exception = "Exception run:\n\n%s\n\n\nPress Entrée to exit.\n" % e

        except Exception as e:
            msg_exception = 'Exception run Python:\n\n' + traceback.format_exc() + "\n\n\nPress Entrée to exit.\n"

    except ALLExcept as e:
        msg_exception = "Exception decode:\n\n%s\n\n\nPress Entrée to exit.\n" % e

    except Exception as e:
        msg_exception = 'Exception decode Python:\n\n' + traceback.format_exc() + "\n\n\nPress Entrée to exit.\n"


    if msg_exception:

        try: input(msg_exception)
        except KeyboardInterrupt:
            # CTRL + C
            print("KeyboardInterrupt")
            sys.exit()
        except EOFError:
            # CTRL + D
            sys.exit()


class Info:

    def __init__(self, variables=None, events=None, path_file=None, path_exe=None):

        self.variables = variables if variables else [{}]
        self.events = events if events else {}

        self.path_exe = path_exe
        self.path_file = path_file

        self.get_event = self.events.get

    def add(self, variables):
        return Info([variables] + self.variables, dict(self.events), self.path_file, self.path_exe)

    def get(self, var, ligne=None):

        for variables in self.variables:
            value = variables.get(var)
            if value is not None:
                return value

        raise NotDefined(var, ligne if ligne else '')

    def set(self, var, value, local=False):

        if not local:
            for variables in self.variables:
                if var in variables:
                    variables[var] = value
                    return

        self.variables[0][var] = value

    def set_event(self, event):

        for var in event.vars:
            if var not in self.events:
                self.events[var] = [event]
            else:
                self.events[var].append(event)