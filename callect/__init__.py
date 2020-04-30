
__version__ = "0.9.0"


from .errors import NotDefined, ALLExcept

from .decode import decode

from .built_in import fonctions_intégrées

import traceback

import time


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


def run(data, path, *, time=False):

    try:
        data = decode(data, path)

        try:

            if time:
                print(calcul_time(lambda: data(Info([fonctions_intégrées], path=path).add({}))))

            else:
                data(Info([fonctions_intégrées], path=path).add({}))

        except ALLExcept as e:
            print('Exception run:\n\n%s' % e)
            input("\n\nPress Entrée to exit.")

        except Exception as e:
            print('Exception Python:\n')
            print(traceback.format_exc())
            input("\n\nPress Entrée to exit.")

    except ALLExcept as e:
        print('Exception decode:\n\n%s' % e)
        input("\n\nPress Entrée to exit.")

    except Exception as e:
        print('Exception Python:\n')
        print(traceback.format_exc())
        input("\n\nPress Entrée to exit.")


class Info:

    def __init__(self, variables=None, events=None, path=None):

        self.variables = variables if variables else [{}]
        self.events = events if events else {}

        self.path = path

        self.get_event = self.events.get

    def add(self, variables):
        return Info([variables] + self.variables, dict(self.events), self.path)

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
                self.events[var] = []
            self.events[var].append(event)