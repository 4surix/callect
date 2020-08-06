from ..base import Base, Prio
from ..conditions import (
    Ega, Sup, Inf, SupOrEga, InfOrEga, Not, 
    And, Or, XAnd, XOr, In
)
from ..redirec import RedirecPoint, RedirecItem
from ..errors import SyntaxIncorrect, NotCompatible
from .var import Var
from .intervalle import Intervalle
from .table import Table
from .txt import Txt


class Event(Base):

    def __call__(self, variables):

        variables.set_event(self)

    def end__(self, cont):

        if len(self.value) == 4:
            """
            event keypress 'Space' 
            (pause_activée == 1) [
                DIRECTION = 'X'
            ]
            """
            self.type, self.key, self.conditions, self.bloc = self.value


            value = self.type.value

            if value == 'keypress':

                if self.key.__class__ == Var:
                    self.key_is_var = True

                elif self.key.__class__ == Txt:
                    self.key_is_var = False

                else:
                    raise SyntaxIncorrect(self.ligne__)

                self.key = self.key.value

            else:
                raise SyntaxIncorrect(self.ligne__)

            self.type = value


            if self.conditions.__class__ == Prio:
                self.conditions = self.conditions.value[0]


        elif len(self.value) == 3:
            """
            event changevars 
            (pomme == 1) [
                print{'a'}
            ]

            event changedate
            (seconde == 0) [
                print{'Nouvelle minute !'}
            ]

            event keypress 'Space' [
                DIRECTION = 'X'
            ]
            """
            self.type, self.conditions, self.bloc = self.value

            self.type = value = self.type.value

            if value in ['changevars', 'changedate']:
                pass

            elif value == 'keypress':

                self.key = self.conditions

                if self.key.__class__ == Var:
                    self.key_is_var = True

                elif self.key.__class__ == Txt:
                    self.key_is_var = False

                else:
                    raise SyntaxIncorrect(self.ligne__)

                self.key = self.key.value

                self.conditions = None

            else:
                raise SyntaxIncorrect(self.ligne__)


            if self.conditions.__class__ == Prio:
                self.conditions = self.conditions.value[0]


        else:
            raise SyntaxIncorrect(self.ligne__)


        ### Recolte de toutes les variables

        self.vars = vars__ = []

        if self.type != 'changevars':
            return

        types = (
            Ega, Sup, Inf, SupOrEga, InfOrEga, Not, 
            And, Or, XAnd, XOr, In
        )


        def recolte(elements):

            for i, element in enumerate(elements):

                type_element = element.__class__

                if type_element == Table:
                    recolte(element.list__)
                    recolte(element.dict__.keys())
                    recolte(element.dict__.values())

                elif (type_element == Var
                or    type_element == RedirecPoint):
                    vars__.append(element.value)

                elif type_element == Prio:
                    recolte(element.value)

                elif type_element in types:
                    recolte(element.value)

                elif type_element == Hidden:
                    elements[i] = element.objet


        element = self.conditions

        type_element = element.__class__

        if (type_element == Var
        or  type_element == RedirecPoint):
            vars__.append(element.value)

        elif type_element in types:
            recolte(element.value)

        else:
            raise SyntaxIncorrect(self.ligne__)


class Hidden(Base):

    def __call__(self, variables, setvar=None, is_global=False):

        return self.objet(
            variables, 
            setvar=setvar, is_global=is_global, hidden=True
        )

    def end__(self, cont):

        self.objet = self.value[0]

        type_name = self.objet.__class__.__name__

        if type_name not in ['Var', 'RedirecPoint']:
            raise SyntaxIncorrect(self.ligne__)