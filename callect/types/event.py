from ..base import Base, Prio

from ..conditions import Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr, In

from ..redirec import RedirecPoint, RedirecItem

from ..errors import SyntaxIncorrect

from .var import Var
from .intervalle import Intervalle
from .table import Table


class Event(Base):

    def __call__(self, variables):

        variables.set_event(self)

    def end__(self, cont):

        if len(self.value) == 3:
            """
            $ vars (banane == 'verte') [
                print{'Pas mûr !'}
            ]
            """
            self.type, self.conditions, self.bloc = self.value

            if self.type.value not in ['vars', 'date', 'keys']:
                raise SyntaxIncorrect(self.ligne__)

            self.type = self.type.value

        # ===
        # Disparait après la v1.0.0pre3
        elif len(self.value) == 2:
            """
            $ (banane == 'verte') [
                print{'Pas mûr !'}
            ]
            """
            self.conditions, self.bloc = self.value

            self.type = 'vars'
        # ===

        else:
            raise SyntaxIncorrect(self.ligne__)


        ### Recolte de toutes les variables

        self.vars = vars__ = []

        types = (Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr, In, Intervalle, Prio)


        def recolte(elements):

            for element in elements:

                type_element = element.__class__

                if type_element == Table:
                    recolte(element.value__)

                elif type_element == Var:
                    vars__.append(element.value)

                elif type_element == RedirecPoint:
                    vars__.append(element.value)

                elif type_element in types:
                    recolte(element.value)


        element = self.conditions

        type_element = element.__class__

        if type_element == Table:
            recolte(element.value__)

        elif type_element == Var:
            vars__.append(element.value)

        elif type_element == RedirecPoint:
            vars__.append(element.value)

        elif type_element in types:
            recolte(element.value)
