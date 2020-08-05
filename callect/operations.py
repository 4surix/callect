from .base import Base, SigneAction
from .errors import NotSupported


class Operation(Base):

    def end__(self, cont):

        self.premier_objet, *self.objets = [
            element 
            for element in self.value
            if element != SigneAction
        ]


class Add(Operation): # Addition

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: add__ = e1['add__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'add__')

            e1 = add__(variables, [e2])

        return e1


class Sub(Operation): # Soustraction

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: sub__ = e1['sub__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'sub__')

            e1 = sub__(variables, [e2])

        return e1


class Div(Operation): # Division

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: div__ = e1['div__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'div__') 

            e1 = div__(variables, [e2])

        return e1


class Mod(Operation): # Modulo

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: mod__ = e1['mod__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'mod__') 

            e1 = mod__(variables, [e2])

        return e1


class Mul(Operation): # Multiplication

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: mul__ = e1['mul__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'mul__') 

            e1 = mul__(variables, [e2])

        return e1


class Exp(Operation): # Exposant

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: exp__ = e1['exp__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'exp__')

            e1 = exp__(variables, [e2])

        return e1


class Rac(Operation): # Racine

    def __call__(self, variables):

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: rac__ = e1['rac__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'rac__')

            e1 = rac__(variables, [e2])

        return e1