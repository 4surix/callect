from ..base import Base

from .nbr import Pos, Neg, Nul, mk_nbr

from ..errors import NotCompatible


class Intervalle(Base):

    def __call__(self, variables):

        debut = self.value[0]
        fin = self.value[1]

        if len(self.value) > 2:
            step = self.value[2]
        else:
            step = Pos(1)
            step.ligne__ = self.ligne__


        types_valide = (Pos, Neg, Nul)

        debut = debut(variables)

        if not debut.__class__ in types_valide: 
            raise NotCompatible(self, debut, self.ligne__)

        fin = fin(variables)

        if not fin.__class__ in types_valide:
            raise NotCompatible(self, fin, self.ligne__)

        step = step(variables)

        if not step.__class__ in types_valide:
            raise NotCompatible(self, step, self.ligne__)


        self.debut:int = debut.value
        self.fin:int = fin.value + 1
        self.step:int = step.value


        self.range = range(self.debut, self.fin, self.step)
        return self


    def __iter__(self):

        for value in self.range:
            yield mk_nbr(value)


    def __str__(self):

        return ';'.join(self.value)