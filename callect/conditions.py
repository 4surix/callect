from .base import Base

from .errors import NotSupported

from .types.bool import True__, False__


class Not(Base): # Not
    
    def __call__(self, variables):

        return [True__, False__][bool(self.value[0](variables))]


class Ega(Base): # Egal

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: ega__ = e1['ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'ega__')

            if not ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != Ega]


class EgaObj(Base): # Egal

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: ega_obj__ = e1['ega_obj__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'ega_obj__')

            if not ega_obj__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class Sup(Base): # Supérieur

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: sup__ = e1['sup__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'sup__')

            if not sup__(variables, [e2]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != Sup]


class Inf(Base): # Inférieur

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: inf__ = e1['inf__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'inf__')

            if not inf__(variables, [e2]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != Inf]


class SupOrEga(Base): # Supérieur ou égal

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: sup_ega__ = e1['sup_ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'sup_ega__')

            if not sup_ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != SupOrEga]


class InfOrEga(Base): # Inférieur ou égal

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: inf_ega__ = e1['inf_ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'inf_ega__')

            if not inf_ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != InfOrEga]


class In(Base): # Contient

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: in__ = e2['in__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'in__')

            if not in__(variables, [e1]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != In]


class RemIn(Base): # Contient

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: remin__ = e2['remin__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'remin__')

            if not remin__(variables, [e1]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != In]



class PopIn(Base): # Contient

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try: popin__ = e2['popin__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'popin__')

            if not popin__(variables, [e1]):
                return False__

            e1 = e2

        return True__

    def end__(self, cont):

        self.value = [v for v in self.value if v != In]


class And(Base): # ET

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try:
                if not e1['and__'](variables, [e2]):
                    return False__

            except (KeyError, AttributeError):
                if not (e1 and e2):
                    return False__

            e1 = e2

        return True__


class Or(Base): # OU

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            try:
                if not e1['or__'](variables, [e2]):
                    return False__

            except (KeyError, AttributeError):
                if not (e1 or e2):
                    return False__

            e1 = e2

        return True__


class XAnd(Base): # XET

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            if getattr(e1, 'xand__', None):
                if not e1.xand__(variables, [e2]):
                    return False__

            else:
                if (e1 and e2) or not (e1 or e2):
                    return False__

            e1 = e2

        return True__


class XOr(Base): # XOU

    def __call__(self, variables):

        e1 = None

        for e2 in self.value:

            if e1 is None:
                e1 = e2(variables)
                continue

            e2 = e2(variables)

            if getattr(e1, 'xor__', None):
                if not e1.xor__(variables, [e2]):
                    return False__

            else:
                if (e1 or e2) and not (e1 and e2):
                    return False__

            e1 = e2

        return True__