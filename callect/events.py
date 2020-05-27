
### Capture de touche clavier 
# Source du code pour récupérer les touches: https://stackoverflow.com/a/31736883

import platform

name_system = platform.system()


if name_system == 'Linux':

    import sys, tty, termios

    def getKey() -> str:

        key = ''
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            # Définit le mode du descripteur de fichier fd à row
            tty.setraw(fd)
            # Lis le prochain caractère
            key = sys.stdin.read(1)

        finally:
            # Remet les valeurs comme avant de fd après la transmission de toute sortie en file d’attente
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return key


elif name_system == 'Windows':

    from msvcrt import getch

    def getKey() -> str:

        return chr(getch()[0])


elif name_system == 'Darwin':

    import Carbon

    EventAvail = Carbon.Evt.EventAvail
    GetNextEvent = Carbon.Evt.GetNextEvent

    def getKey() -> str:

        if EventAvail(0x0008)[0] == 0:
            return ''

        else:
            what, msg, when, where, mod = GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)


### Thread

import sys
import time

from threading import Thread


from .types.txt import mk_txt
from .types.nbr import mk_nbr
from .types.table import mk_table


class Time(Thread):

    def __init__(self, variables):
        Thread.__init__(self)

        self.running = True

        self.variables = variables

    def run(self):

        events = self.variables.events_date

        while 1:

            date = mk_table(_list=[mk_nbr(nbr) for nbr in time.gmtime()[:6]])


            if not self.running:
                # L'orsque le thread est arrété
                return


            if events:
                for event in events:
                    variables = event.variables
                    variables.variables[0]['date__'] = date
                    if event.conditions(variables):
                        event.bloc(variables)


            time.sleep(1)


class Key(Thread):

    def __init__(self, variables):
        Thread.__init__(self)

        self.running = True

        self.variables = variables

    def run(self):

        events = self.variables.events_keys

        while 1:

            if not self.running:
                # L'orsque le thread est arrété
                return


            if events:

                key = getKey()


                if not self.running:
                    # L'orsque le thread est arrété
                    return


                # J'ai mit les mêmes noms des touches que Tkinter

                if key == '\x08':
                    key = 'BackSpace'

                elif key == '\x1b':
                    key = 'Escape'

                elif key == '\r':
                    key = 'Return'

                elif key == '\t':
                    key = 'Tab'

                elif key == '\xe0':

                    key = getKey()

                    if key == 'H':
                        key = 'Up'

                    elif key == 'P':
                        key = 'Down'

                    elif key == 'K':
                        key = 'Left'

                    elif key == 'M':
                        key = 'Right'

                    elif key == 'S':
                        key = 'Delete'

                    elif key == 'R':
                        key = 'Insert'

                    elif key == 'Q':
                        key = 'PageUp'

                    elif key == 'I':
                        key = 'PageDown'

                    elif key == 'G':
                        key = 'Begin'

                    elif key == 'O':
                        key = 'End'

                    elif key == '\x85':
                        key = 'F11'

                    elif key == '\x86':
                        key = 'F12'

                elif key == '\x00':

                    key = getKey()

                    if key == ';':
                        key = 'F1'

                    elif key == '<':
                        key = 'F2'

                    elif key == '=':
                        key = 'F3'

                    elif key == '>':
                        key = 'F4'

                    elif key == '?':
                        key = 'F5'

                    elif key == '@':
                        key = 'F6'

                    elif key == 'A':
                        key = 'F7'

                    elif key == 'B':
                        key = 'F8'

                    elif key == 'C':
                        key = 'F9'

                    elif key == 'D':
                        key = 'F10'


                key = mk_txt(key)

                for event in events:
                    variables = event.variables
                    variables.variables[0]['key__'] = key
                    if event.conditions(variables):
                        event.bloc(variables)


def run(variables):

    # Création des threads
    thread_1 = Time(variables)
    thread_2 = Key(variables)

    # Lancement des threads
    thread_1.start()
    thread_2.start()


    return thread_1, thread_2