
from .base import Base, SigneAction

from .types.nbr import Pos, Neg
from .types.objet import Inst
from .types.txt import Txt

from .errors import NotCompatible, SyntaxIncorrect


class For(Base):

    def __call__(self, variables):

        try:
            for _, element in self.conteneur(variables):

                self.var(variables, setvar=element)

                try: self.bloc(variables)
                except ContinueIteration:
                    pass

        except StopIteration:
            pass

    def end__(self, cont):

        self.value = [v for v in self.value if v != SigneAction]

        if len(self.value) == 3:
            self.var, self.conteneur, self.bloc = self.value

        else:
            raise SyntaxIncorrect(self.ligne__)


class Repeat(Base):

    def __call__(self, variables):

        value = self.conteneur(variables)

        if value.__class__.__name__ != 'Pos':
            raise NotCompatible(self, value, self.ligne__)

        try:
            for _ in value:
                try: self.bloc(variables)
                except ContinueIteration:
                    pass
                
        except StopIteration:
            pass

    def end__(self, cont):

        if len(self.value) == 2:
            self.bloc = self.value[1]

            value = self.value[0]

            self.conteneur = value

        else:
            raise SyntaxIncorrect(self.ligne__)


class IFor(Base):

    def __call__(self, variables):

        try:
            for index, element in self.conteneur(variables):

                self.index(variables, setvar=index)
                self.var(variables, setvar=element)

                try: self.bloc(variables)
                except ContinueIteration:
                    pass

        except StopIteration:
            pass

    def end__(self, cont):

        self.value = [v for v in self.value if v != SigneAction]

        if len(self.value) == 4:
            self.index, self.var, self.conteneur, self.bloc = self.value

        else:
            raise SyntaxIncorrect(self.ligne__)


class While(Base):

    def __call__(self, variables):

        try:
            while self.conditions(variables):
                try: self.bloc(variables)
                except ContinueIteration:
                    pass

        except StopIteration:
            pass

    def end__(self, cont):

        if len(self.value) == 2:
            self.conditions, self.bloc = self.value

        else:
            raise SyntaxIncorrect(self.ligne__)


class Break(Base):

    def __call__(self, variables):

        raise StopIteration()


class Continue(Base):

    def __call__(self, variables):

        raise ContinueIteration()


class ContinueIteration(Exception):
    pass