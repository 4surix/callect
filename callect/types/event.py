from ..base import Base

from ..conditions import Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr

from ..redirec import RedirecPoint, RedirecItem

from .var import Var
from .intervalle import Intervalle
from .table import Table


class Event(Base):

    def __call__(self, variables):

        variables.set_event(self)

    def call__(self, variables, args=None, kwargs=None):

        if self.conditions(variables):
            for element in self.bloc.value:
                element(variables)

    def end__(self, cont):

        self.conditions, self.bloc = self.value

        self.vars = vars_ = []

        types = (Ega, Sup, Inf, SupOrEga, InfOrEga, Not, And, Or, XAnd, XOr, RedirecPoint, RedirecItem, Intervalle, Table)

        def recolte(elements):
            for element in elements:
                if isinstance(element, types):
                    recolte(element.value)
                elif isinstance(element, Var):
                    vars_.append(str(element))

        recolte(self.conditions.value)