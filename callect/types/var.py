from ..base import Base

from .txt import Txt

from .objet import Inst, Objet

from ..errors import NotItem


class Var(Base):

    def __call__(self, variables, setvar=None, local=False):

        if setvar is not None:
            variables.set(self.value, setvar, local=local)

            events = variables.get_event(self.value)

            if events:
                for event in events:
                    if event.conditions(variables):
                        for element in event.bloc.value:
                            element(variables)

        else:
            value = variables.get(self.value, ligne=self.ligne__)

            if isinstance(value, Inst):

                try: value__ = value['obj__']
                except NotItem:
                    pass
                else:
                    value = value__(variables, [], {})

            elif value.__class__ == Objet and value.callable_without_call:

                value = value(variables, [], {})


            return value

    def __hash__(self):
        return hash(self.value)

    def end__(self, cont):

        self.value = ''.join(str(e) for e in self.value)