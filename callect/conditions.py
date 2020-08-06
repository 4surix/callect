from .base import Base, SigneAction
from .errors import NotSupported
from .types.bool import True__, False__


class Comparaison(Base):

    def end__(self, cont):

        self.premier_objet, *self.objets = [
            element 
            for element in self.value
            if element != SigneAction
        ]


class Ega(Comparaison): # Egal

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: ega__ = e1['ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'ega__')

            if not ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class EgaObj(Comparaison): # Egal

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: ega_obj__ = e1['ega_obj__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'ega_obj__')

            if not ega_obj__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class Sup(Comparaison): # Supérieur

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: sup__ = e1['sup__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'sup__')

            if not sup__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class Inf(Comparaison): # Inférieur

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: inf__ = e1['inf__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'inf__')

            if not inf__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class SupOrEga(Comparaison): # Supérieur ou égal

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: sup_ega__ = e1['sup_ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'sup_ega__')

            if not sup_ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class InfOrEga(Comparaison): # Inférieur ou égal

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: inf_ega__ = e1['inf_ega__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'inf_ega__')

            if not inf_ega__(variables, [e2]):
                return False__

            e1 = e2

        return True__


class In(Comparaison): # Contient

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: in__ = e2['in__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'in__')

            if not in__(variables, [e1]):
                return False__

            e1 = e2

        return True__


class RemIn(Comparaison): # Contient

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: remin__ = e2['remin__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'remin__')

            if not remin__(variables, [e1]):
                return False__

            e1 = e2

        return True__


class PopIn(Comparaison): # Contient

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        e1 = self.premier_objet(variables)

        for e2 in self.objets:

            e2 = e2(variables)

            try: popin__ = e2['popin__']
            except (KeyError, AttributeError):
                raise NotSupported(e2, 'popin__')

            if not popin__(variables, [e1]):
                return False__

            e1 = e2

        return True__


class ComparaisonBooleenne(Base):

    def end__(self, cont):

        self.objets = [
            element 
            for element in self.value
            if element != SigneAction
        ]


class Not(ComparaisonBooleenne): # Not
    
    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        objet = self.objets[0](variables)

        try: bool__ = objet['bool__']
        except (KeyError, AttributeError):
            raise NotSupported(objet, 'bool__')

        if bool__(variables):
            return False__
        else:
            return True__


class And(ComparaisonBooleenne): # ET

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        for e1 in self.objets:

            e1 = e1(variables)

            try: bool__ = e1['bool__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'bool__')

            if not bool__(variables):
                return False__

        return True__


class Or(ComparaisonBooleenne): # OU

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        for e1 in self.objets:

            e1 = e1(variables)

            try: bool__ = e1['bool__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'bool__')

            if bool__(variables):
                return True__

        return False__


class XAnd(ComparaisonBooleenne): # XET

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        last_bool = None

        for e1 in self.objets:

            e1 = e1(variables)

            try: bool__ = e1['bool__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'bool__')

            e1_bool = bool__(variables)

            if last_bool != e1_bool and last_bool is not None:
                return False__

            last_bool = e1_bool

        return True__


class XOr(ComparaisonBooleenne): # XOU

    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        déjà_true = False

        for e1 in self.objets:

            e1 = e1(variables)

            try: bool__ = e1['bool__']
            except (KeyError, AttributeError):
                raise NotSupported(e1, 'bool__')

            if bool__(variables):
                if déjà_true:
                    return False__
                déjà_true = True

        if déjà_true:
            return True__
        else:
            return False__