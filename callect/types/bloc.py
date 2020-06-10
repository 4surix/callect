from ..base import Base
from .bool import False__, True__


class Bloc(Base):
    
    def __call__(self, variables):

        value = False__

        for element in self.value:
            value = element(variables)

        return value

    def end__(self, cont):

        objet = None

        for value in self.value:

            if value.__class__.__name__ in ['Txt', 'Pos', 'Neg', 'Nul', 'Table', 'Intervalle', 'IsExist']:
                if objet is not None:
                    raise Exception("%s Mettre un type '%s' à coter d'un type '%s' est inutile." % (
                        value.ligne__, objet.__class__.__name__, value.__class__.__name__)
                    )
                else:
                    objet = value
            else:
                objet = None