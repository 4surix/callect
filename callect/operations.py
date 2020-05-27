from .base import Base

from .errors import NotSupported


class Add(Base): # Addition

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: add__ = e1['add__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'add__')

            e1 = add__(variables, [e2])

        return e1


class Sub(Base): # Soustraction

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: sub__ = e1['sub__']
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'sub__')

            e1 = sub__(variables, [e2])

        return e1


class Div(Base): # Division

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: e1 = e1['div__'](variables, [e2])
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'div__') 

        return e1


class Mod(Base): # Modulo

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: e1 = e1['mod__'](variables, [e2])
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'mod__') 

        return e1


class Mul(Base): # Multiplication

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: e1 = e1['mul__'](variables, [e2])
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'mul__') 

        return e1


class Exp(Base): # Exposant

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: e1 = e1['exp__'](variables, [e2])
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'exp__') 

        return e1


class Rac(Base): # Racine

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: e1 = e1['rac__'](variables, [e2])
            except (AttributeError, KeyError):
                raise NotSupported(e1, 'rac__')

        return e1