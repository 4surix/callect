from .base import Base

from .errors import NotCompatible

from .types.txt import mk_txt
from .types.objet import CallObjetWithParent


class RedirecItem(Base):

    def __call__(self, variables, setvar=None, local=False):

        value = self.var(variables)

        for element in self.elements:
            element = element(variables)
            element.ligne__ = self.ligne__
            value = value[element]


        item = self.item(variables)
        item.ligne__ = self.ligne__


        if setvar is not None:
            value[item] = setvar

        else:
            value = value[item]
            if value.__class__ == CallObjetWithParent and value.value.callable_without_call:
                value = value(variables, [], {})


        return value

    def end__(self, cont):

        self.var = self.value.pop(0)
        self.item = self.value.pop()
        self.elements = self.value


class RedirecPoint(Base):

    def __call__(self, variables, setvar=None, local=False):

        value = self.var(variables)

        for element in self.elements:
            value = value[element]


        if setvar is not None:
            value[self.item] = setvar


            for event in variables.get_event(str(self.var), []):
                event.call__(variables)

        else:
            value = value[self.item]
            if value.__class__ == CallObjetWithParent and value.value.callable_without_call:
                value = value(variables, [], {})


        return value

    def end__(self, end):

        for index, value in enumerate(self.value[1:]):
            if value.__class__.__name__ != 'Var':
                raise NotCompatible(value, self, self.ligne__)

            value = mk_txt(value.value)
            
            value.ligne__ = self.ligne__

            self.value[index+1] = value


        self.var = self.value.pop(0)
        self.item = self.value.pop()
        self.elements = self.value