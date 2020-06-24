
from .base import Base, SigneAction
from .errors import AllNonexistent, NotCompatible


class Typ(Base): # Type var

    def __call__(self, variables, setvar=None, is_global=False, hidden=False):

        obj = self.type(variables)

        if setvar is not None:

            if obj.__name__ != setvar.__class__.__name__:
                setvar = obj.call__(variables, [setvar], {})

            self.objet(variables, setvar=setvar, is_global=is_global, hidden=hidden)

        else:

            value = self.objet(variables)

            if obj.__name__ != value.__class__.__name__:
                value = obj.call__(variables, [value], {})

            return value

    def __str__(self):
        return '%s:%s' % self.objet, self.type

    def __eq__(self, obj):
        # L'ors de la fusion des dict pour le call__ des objets
        return self.objet.value == obj.value

    def __hash__(self):
        return hash(self.objet.value)

    def end__(self, cont):
        self.objet, self.type = self.value

        if self.objet.__class__.__name__ not in (
                'Var', 'Txt', 'Pos', 'Neg', 'Nul', 'Prio', 'RedirecPoint'
            ):
            raise NotCompatible(self, self.objet, self.ligne__)

        if self.type.__class__.__name__ not in ('Var', 'RedirecPoint'):
            raise NotCompatible(self, self.type, self.ligne__)


class Asi(Base): # Asignement

    def __call__(self, variables):

        value = self.objet(variables)

        for element in self.elements:
            element(variables, setvar=value)

    def __iter__(self):
        for value in self.value:
            yield value

    def end__(self, cont):
        *self.elements, self.objet = [v for v in self.value if v != SigneAction]

        # Très important, permet de faire dans le bon ordre.
        # a = b = c = 1
        # D'abbord c puis b puis a.
        # Cela évite des beugs comme l'assigment d'item dans des tables.
        self.elements = self.elements[::-1]


class Global(Base):

    def __call__(self, variables, setvar=None):

        return self.objet(variables, setvar=setvar, is_global=True)

    def end__(self, cont):
        self.objet = self.value[0]

        type_name = self.objet.__class__.__name__

        if type_name not in ['Var', 'Typ', 'Hidden']:
            raise NotCompatible(self, self.objet, self.ligne__)


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

        self.value = [v for v in self.value if v != SigneAction]

        types_valables = [
            'Var', 'RedirecItem', 'RedirecPoint', 'Txt', 'Pos', 'Neg', 'Nul',
            'Table', 'Objet', 'Intervalle'
        ]

        for value in self.value:
            if value.__class__.__name__ not in types_valables:
                raise NotCompatible(self, value, self.ligne__)
