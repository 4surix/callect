from ..base import Base, Prio

from ..conditions import Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr

from ..redirec import RedirecPoint, RedirecItem

from .var import Var
from .intervalle import Intervalle
from .table import Table


class Event(Base):

    def __call__(self, variables):

        variables.set_event(self)

    def end__(self, cont):

        self.conditions, self.bloc = self.value


        # Recolte de toutes les variables

        self.vars = vars__ = []


        types = (Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr, Intervalle, Prio)


        def recolte(elements):

            for element in elements:

                type_element = element.__class__

                if type_element == Table:
                    recolte(element.__dict__['value'])

                elif type_element == Var:
                    vars__.append(element.value)

                elif type_element == RedirecPoint:
                    vars__.append(element.value)

                elif type_element in types:
                    recolte(element.value)


        element = self.conditions

        type_element = element.__class__

        if type_element == Table:
            recolte(element.__dict__['value'])

        elif type_element == Var:
            vars__.append(element.value)

        elif type_element == RedirecPoint:
            vars__.append(element.value)

        elif type_element in types:
            recolte(element.value)
