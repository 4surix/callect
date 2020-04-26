from .base import Base

from .types.nbr import Pos, Neg
from .types.objet import Inst
from .types.txt import Txt

from .conditions import In

from .errors import NotCompatible, SyntaxIncorrect


class For(Base):

    def __call__(self, variables):

        try:
            for element in self.conteneur(variables):
                self.var(variables, setvar=element)
                self.bloc(variables)

        except StopIteration:
            pass

    def end__(self, cont):

        self.value = [v for v in self.value if v != In]

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
            for element in value:
                self.bloc(variables)
                
        except StopIteration:
            pass

    def end__(self, cont):

        if len(self.value) == 2:
            self.bloc = self.value[1]

            value = self.value[0]

            if value.__class__.__name__ not in ['Pos', 'Var', 'RedirecItem', 'RedirecPoint', 'Call']:
                raise NotCompatible(self, value, self.ligne__)

            self.conteneur = value

        else:
            raise SyntaxIncorrect(self.ligne__)


class IFor(Base):

    def __call__(self, variables):

        args = {}

        cont = self.conteneur(variables)


        name_type_cont = cont.__class__.__name__


        if name_type_cont == 'Table':
            elements = []
            add = elements.append

            index = 0

            for value in cont.list__:
                index += 1
                add((Pos(index), value))

            for key, value in cont.dict__.items():
                add((key, value))

        elif name_type_cont == 'Txt':
            elements = [(Pos(index), Txt(value)) for index, value in enumerate(cont.value)]

        elif name_type_cont == 'Pos':
            elements = [(neg, pos) for neg, pos in zip([Neg(value) for value in range(-1, cont.value-1, -1)], [Pos(value) for value in range(1, cont.value+1)])]

        elif name_type_cont == 'Neg':
            elements = [(pos, neg) for pos, neg in zip([Pos(value) for value in range(1, cont.value+1)], [Neg(value) for value in range(-1, cont.value-1, -1)])]

        elif isinstance(cont, Inst):
            elements = [(k, v) for k, v in cont.__dict__.items() if k[-2:] != '__']

        else:
            raise NotCompatible(self, cont, self.ligne__) 


        try:
            for index, element in elements:
                self.index(variables, setvar=index)
                self.var(variables, setvar=element)
                self.bloc(variables)

        except StopIteration:
            pass

    def end__(self, cont):

        self.value = [v for v in self.value if v != In]

        if len(self.value) == 4:
            self.index, self.var, self.conteneur, self.bloc = self.value

        else:
            raise SyntaxIncorrect(self.ligne__)


class While(Base):

    def __call__(self, variables):

        while self.conditions(variables):
            self.bloc(variables)

    def end__(self, cont):

        if len(self.value) == 2:
            self.conditions, self.bloc = self.value

        else:
            raise SyntaxIncorrect(self.ligne__)


class Break(Base):

    def __call__(self, variables):

        raise StopIteration('') 