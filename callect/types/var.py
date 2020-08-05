from ..base import Base

from .txt import mk_txt

from .objet import Inst, Objet

from ..errors import NotItem


name_obj__ = mk_txt('obj__')


class Var(Base):

    def __call__(self, variables, setvar=None, is_global=False, hidden=False):

        if setvar is not None:
            variables.set(self.value, setvar, is_global=is_global)

            if not hidden:
                events = variables.get_event(self.value)

                if events:
                    for event in events:
                        if event.conditions(variables):
                            event.bloc(variables)

        else:
            value = variables.get(self.value, is_global=is_global, ligne=self.ligne__)

            if isinstance(value, Inst):
                """
                @'pouet' self {
                    'obj__' @[return 'pouf']
                } [return self]
                pouet == 'pouf'
                """

                try: value__ = value[name_obj__]
                except NotItem:
                    pass
                else:
                    value = value__(variables, [], {})

            elif value.__class__ == Objet and value.callable_without_call:
                """
                @'pouet' [
                    return 'pouf'
                ]
                pouet == 'pouf'
                """

                value = value(variables, [], {})


            return value

    def __hash__(self):
        return hash(self.value)

    def end__(self, cont):

        self.value = ''.join(str(e) for e in self.value)