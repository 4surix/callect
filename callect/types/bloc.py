from ..base import Base, SigneAction
from ..errors import SyntaxIncorrect
from .bool import False__, True__


class Bloc(Base):
    
    def __call__(self, variables):

        value = False__

        while True:

            try:
                for element in self.value:
                    value = element(variables)

                return value

            except Up:
                # [  ...
                #    up 1
                #    ...
                # ]
                continue

            except Down:
                # [  ...
                #    down 1
                #    ...
                # ]
                break

        return value

    def end__(self, cont):

        # [pomme = 1, poire = pomme = 13, print{poire}]
        self.value = [v for v in self.value if v != SigneAction]

        objet = None

        for value in self.value:

            if value.__class__.__name__ in [
                    'Txt', 'Pos', 'Neg', 'Nul', 'Table', 
                    'Intervalle', 'IsExist'
                ]:
                if objet is not None:
                    raise SyntaxIncorrect(self.ligne__)
                else:
                    objet = value
            else:
                objet = None


class Up(Base, Exception):

    def __call__(self, variables):

        if self.condition(variables):
            raise self

        return False__

    def end__(self, cont):

        if len(self.value) == 1:
            self.condition = self.value[0]

        else:
            raise SyntaxIncorrect(self.ligne__)


class Down(Base, Exception):

    def __call__(self, variables):

        if self.condition(variables):
            raise self

        return False__

    def end__(self, cont):

        if len(self.value) == 1:
            self.condition = self.value[0]

        else:
            raise SyntaxIncorrect(self.ligne__)