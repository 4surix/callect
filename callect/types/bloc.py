from ..base import Base


class Bloc(Base):
    
    def __call__(self, variables):

        for element in self.value:
            element(variables)

    def end__(self, cont):

        is_var = None

        for value in self.value:

            if value.__class__.__name__ in ['Var', 'Txt', 'Pos', 'Neg', 'Nul', 'Table', 'Intervalle', 'IsExist']:
                if is_var is not None:
                    raise Exception("%s Mettre '%s' à coter de '%s' est inutile." % (value.ligne__, type(is_var).__name__, type(value).__name__))
                else:
                    is_var = value
            else:
                is_var = None

        self.ligne__ = str(cont.ligne)