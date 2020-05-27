from ..base import Base


class Bloc(Base):
    
    def __call__(self, variables):

        for element in self.value:
            element(variables)

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