from .base import Base

from .errors import AllNonexistent, NotCompatible


class Typ(Base): # Type var

    def __call__(self, variables, setvar=None, local=False):

        obj = self.type(variables)

        if setvar is not None:

            if obj.__name__ != setvar.__class__.__name__:
                setvar = obj.call__(variables, [setvar], {})

            self.objet(variables, setvar=setvar, local=local)

        else:

            value = self.objet(variables)

            if obj.__name__ != value.__class__.__name__:
                value = obj.call__(variables, [value], {})

            return value

    def end__(self, cont): 
        self.objet, self.type = self.value

        type_name = type(self.type).__name__

        if type_name != 'Var':
            raise NotCompatible(self.type, self, self.ligne__)


class Asi(Base): # Asignement
    
    def __call__(self, variables):

        value = self.objet(variables)

        for element in self.elements:
            element(variables, setvar=value)

    def __iter__(self):
        for value in self.value:
            yield value

    def end__(self, cont):
        *self.elements, self.objet = [v for v in self.value if v != Asi]


class Local(Base): # Local

    def __call__(self, variables, setvar=None):

        self.objet(variables, setvar=setvar, local=True)

    def end__(self, cont):
        self.objet = self.value[0]

        type_name = type(self.objet).__name__

        if type_name not in ['Var', 'Typ']:
            raise NotCompatible(self.objet, self, self.ligne__)


class IsExist(Base): # Verification existe

    def __call__(self, variables):

        for value in self.value:
            try:
                return value(variables)
            except:
                pass

        raise AllNonexistent(self, self.ligne__)

    def end__(self, cont):
        self.ligne__ = str(cont.ligne)

        self.value = [v for v in self.value if v != IsExist]

        types_valables = ['Var', 'RedirecItem', 'RedirecPoint', 'Txt', 'Pos', 'Neg', 'Nul', 'Table', 'Objet', 'Intervalle']

        for value in self.value:
            if value.__class__.__name__ not in types_valables:
                raise NotCompatible(value, self, self.ligne__)