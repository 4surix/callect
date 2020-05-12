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


        self.debut__ = debut__ = int(debut.value)

        self.debut = debut__ - 1 if debut__ > 0 else debut__ # 2;8;1 --> 1;8;1    -6;8;1 --> -6;8:1
        self.fin = int(fin.value - 1 if fin.value < 0 else fin.value) # 5;7 --> 5;7     -1;-4;-1 --> -1;-5;-1
        self.step = int(step.value)


        self.range = range(
            self.debut__, 
            self.fin + 1 if self.fin > 0 else self.fin, # 1;3;1 --> 1;4;1    1;-3;1 --> 1;-3;1
            self.step
        )

        return self


    def __iter__(self):

        for value in self.range:
            yield mk_nbr(value)


    def __str__(self):

        return '%s;%s;%s' % (self.debut__, self.fin, self.step)


    def end__(self, cont):

        self.value = [v for v in self.value if v != Intervalle]